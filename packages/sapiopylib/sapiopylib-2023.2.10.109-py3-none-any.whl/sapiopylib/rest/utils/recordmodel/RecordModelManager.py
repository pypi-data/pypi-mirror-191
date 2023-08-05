from __future__ import annotations

from typing import List, Dict, Set, Any, Tuple, Type
from weakref import WeakValueDictionary

from buslane.events import EventHandler

from sapiopylib.rest.utils.recordmodel.RecordModelWrapper import WrappedType, RecordModelWrapperUtil, WrappedRecordModel
from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.DataRecord import DataRecord, DataRecordDescriptor
from sapiopylib.rest.pojo.DataRecordBatchUpdate import DataRecordBatchUpdate, DataRecordBatchResult, \
    DataRecordRelationChangePojo
from sapiopylib.rest.utils.DataTypeCacheManager import DataTypeCacheManager
from sapiopylib.rest.utils.MultiMap import SetMultimap
from sapiopylib.rest.utils.recordmodel.PyRecordModel import PyRecordModel
from sapiopylib.rest.utils.recordmodel.RecordModelEventBus import RecordModelEventBus
from sapiopylib.rest.utils.recordmodel.RecordModelEvents import RecordAddedEvent, RecordDeletedEvent, \
    FieldChangeEvent, ChildAddedEvent, ChildRemovedEvent, CommitEvent, RollbackEvent
from sapiopylib.rest.utils.recordmodel.RelationshipPath import RelationshipPath, RelationshipPathDir


class RecordModelManager:
    """
    Record Model Manager helps to keep track of a user session changes and attempt to batch record changes
    into one call.

    This class is observing a singleton pattern per user instance. Simply attempt to construct it with user.
    """
    _event_bus: RecordModelEventBus
    _user: SapioUser
    _inst_man: RecordModelInstanceManager
    _relationship_man: RecordModelRelationshipManager
    _trans_man: RecordModelTransactionManager

    __instances: WeakValueDictionary[SapioUser, RecordModelManager] = WeakValueDictionary()
    __initialized: bool

    def __new__(cls, user: SapioUser):
        """
        Observes singleton pattern per user object.
        """
        obj = cls.__instances.get(user)
        if not obj:
            obj = object.__new__(cls)
            obj.__initialized = False
            cls.__instances[user] = obj
        return obj

    def __init__(self, user: SapioUser):
        if self.__initialized:
            return
        self._event_bus = RecordModelEventBus()
        self._user = user
        self._inst_man = RecordModelInstanceManager(self)
        self._relationship_man = RecordModelRelationshipManager(self)
        self._trans_man = RecordModelTransactionManager(self)
        self.__initialized = True

    @property
    def event_bus(self):
        return self._event_bus

    @property
    def user(self):
        return self._user

    @property
    def instance_manager(self):
        return self._inst_man

    @property
    def relationship_manager(self):
        return self._relationship_man

    @property
    def transaction_manager(self):
        return self._trans_man

    def store_and_commit(self):
        return self._trans_man.commit()

    def rollback(self):
        return self._trans_man.rollback()


class RecordModelInstanceManager:
    """
    Manages record model creation and retention in memory of user context.
    """
    _record_model_manager: RecordModelManager
    __instances: WeakValueDictionary[RecordModelManager, RecordModelInstanceManager] = WeakValueDictionary()
    __initialized: bool

    __known_records_by_type: SetMultimap[str, PyRecordModel]
    __record_by_record_id: Dict[int, PyRecordModel]

    __delete_handler: _InstanceRecordDeletedHandler
    __rollback_handler: _InstanceRecordRollbackHandler
    __commit_handler: _InstanceRecordCommitHandler
    __dt_cache_man: DataTypeCacheManager

    def __new__(cls, record_model_manager: RecordModelManager):
        """
        Observes singleton pattern per record model manager object.
        """
        obj = cls.__instances.get(record_model_manager)
        if not obj:
            obj = object.__new__(cls)
            obj.__initialized = False
            cls.__instances[record_model_manager] = obj
        return obj

    def __init__(self, record_model_manager: RecordModelManager):
        if self.__initialized:
            return
        self.__dt_cache_man = DataTypeCacheManager(record_model_manager.user)
        self._record_model_manager = record_model_manager
        self.__known_records_by_type = SetMultimap()
        self.__record_by_record_id = dict()
        self.__delete_handler = _InstanceRecordDeletedHandler(self)
        record_model_manager.event_bus.subscribe_record_delete_event(self.__delete_handler)
        self.__rollback_handler = _InstanceRecordRollbackHandler(self)
        record_model_manager.event_bus.subscribe_rollback_event(self.__rollback_handler)
        self.__commit_handler = _InstanceRecordCommitHandler(self)
        record_model_manager.event_bus.subscribe_commit_event(self.__commit_handler)
        self.__initialized = True

    def _on_rollback(self):
        all_recs = set(self.__record_by_record_id.values())
        new_records: List[PyRecordModel] = [x for x in all_recs if x.is_new]
        for new_record in new_records:
            self.__known_records_by_type.discard_item(new_record.data_type_name, new_record)
            del self.__record_by_record_id[new_record.record_id]
        modified_records = self.__record_by_record_id.values()
        for modified_record in modified_records:
            modified_record.do_rollback()

    def _on_commit(self):
        all_recs = set(self.__record_by_record_id.values())
        for record in all_recs:
            record.do_commit()
            # Update for records with negative Record ID with a new reference point.
            if record.record_id not in self.__record_by_record_id:
                self.__record_by_record_id[record.record_id] = record
        # Remove all negative record ID references we have now
        negative_record_ids = [x for x in self.__record_by_record_id.keys() if x < 0]
        for record_id in negative_record_ids:
            del self.__record_by_record_id[record_id]

    @property
    def record_model_manager(self):
        return self._record_model_manager

    @property
    def event_bus(self):
        """
        The event bus allows the record models to fire events for various managers handling each event type.

        The default record model system already includes some system events. But you can register more event listeners.
        """
        return self._record_model_manager.event_bus

    @property
    def user(self):
        """
        The user context the record model management will provide services for.
        """
        return self._record_model_manager.user

    def add_new_record(self, data_type_name: str) -> PyRecordModel:
        """
        Add a new record model for a new data record.
        :param data_type_name: the data type name of the new record model
        :return: a root record model for this data type.
        """
        default_field_map: Dict[str, Any] = self.__dt_cache_man.get_default_field_map(data_type_name)
        record = DataRecord(data_type_name, self.user.get_next_temp_record_id(), default_field_map)
        return self._get_or_add_record(record)

    def add_new_record_of_type(self, wrapper_type: Type[WrappedType]) -> WrappedType:
        """
        Add a new wrapped record model for a new data record.
        :param wrapper_type: the wrapper class (type) of the new record model
        :return: a new wrapped record model of the wrapped class type.
        """
        dt_name: str = wrapper_type.get_wrapper_data_type_name()
        py_model = self.add_new_record(dt_name)
        wrapped_model: WrappedType = RecordModelWrapperUtil.wrap(py_model, wrapper_type)
        return wrapped_model

    def add_new_records(self, data_type_name: str, num_records: int) -> List[PyRecordModel]:
        """
        Add multiple record models for multiple new data records.
        :param data_type_name: the data type name of the new record models.
        :param num_records: Number of records to be added.
        :return: a list of new record models.
        """
        ret: List[PyRecordModel] = list()
        for i in range(num_records):
            ret.append(self.add_new_record(data_type_name))
        return ret

    def add_new_records_of_type(self, num_records: int, wrapper_type: Type[WrappedType]) -> List[WrappedType]:
        """
        Add multiple wrapped record models for multiple new data records.
        :param num_records:the number of records to be added.
        :param wrapper_type: the wrapper class type
        :return: A list of new wrapped record models of wrapper class type.
        """
        ret: List[WrappedType] = list()
        for i in range(num_records):
            ret.append(self.add_new_record_of_type(wrapper_type))
        return ret

    def add_existing_record(self, record: DataRecord) -> PyRecordModel:
        """
        Import an existing data record as a record model.

        If the record model for this data record has already been imported in this record model manager, this call
        will return the existing object, instead of creating a new object.
        :param record: the data record to be imported as a record model
        :return: the imported record model singleton under the record model manager.
        """
        return self._get_or_add_record(record)

    def add_existing_record_of_type(self, record: DataRecord, wrapper_type: Type[WrappedType]) -> WrappedType:
        """
        Import an existing data record as a wrapped record model.

        If the record model for this data record has already been imported in this record model manager, this call
        will return the existing object, instead of creating a new object.
        :param record: the data record to be imported as a record model
        :param wrapper_type: the wrapper class type
        :return: the imported record model singleton wrapped by the class type.
        """
        py_model = self.add_existing_record(record)
        wrapped_model: WrappedType = RecordModelWrapperUtil.wrap(py_model, wrapper_type)
        return wrapped_model

    def add_existing_records(self, record_list: List[DataRecord]) -> List[PyRecordModel]:
        """
        Import multiple existing data records as record models.

        If the record model for any record has already been imported in this record model manager, this call shall
        retrieve the existing object in its place in the list, instead of creating a new object.
        :param record_list: the data record list to be imported as record models.
        :return: the imported record model list.
        """
        return [self._get_or_add_record(record) for record in record_list]

    def add_existing_records_of_type(self, record_list: List[DataRecord], wrapper_type: Type[WrappedType]) \
            -> List[WrappedType]:
        """
        Import multiple existing data records as wrapped record models.

        If the record model for any record has already been imported in this record model manager, this call shall
        retrieve the existing object in its place in the list, instead of creating a new object.
        :param record_list: the data record list to be imported as record models.
        :param wrapper_type: the imported wrapped record model list.
        :return:
        """
        return [self.add_existing_record_of_type(record, wrapper_type) for record in record_list]

    def get_known_record_with_record_id(self, record_id: int):
        """
        Retrieve an existing root record model by providing its Record ID.
        :param record_id: the record ID used to retrieve the root record model. This can be a negative number for
        new records that has not been stored yet.
        :return: the root record model in the cache. If such a record does not exist, return None.
        """
        return self.__record_by_record_id.get(record_id)

    @staticmethod
    def unwrap(model: WrappedRecordModel) -> PyRecordModel:
        """
        Unwrap a record model to its root model.
        :param model: the wrapped record model
        :return: the root record model
        """
        return RecordModelWrapperUtil.unwrap(model)

    @staticmethod
    def wrap(model: PyRecordModel, wrapper_type: Type[WrappedType]) -> WrappedType:
        """
        Wrap the record model with a decorator type.
        :param model the root record model to wrap
        :param wrapper_type the wrapper class type to wrap to
        :return the wrapped record model object
        """
        return RecordModelWrapperUtil.wrap(model, wrapper_type)

    @staticmethod
    def unwrap_list(models: List[WrappedRecordModel]) -> List[PyRecordModel]:
        """
        Unwrap a list of record models to its root models as another list.
        :param models list of wrapped record models, to unwrap
        :return a list of unwrapped record models in the same order.
        """
        return RecordModelWrapperUtil.unwrap_list(models)

    @staticmethod
    def wrap_list(models: List[PyRecordModel], wrapper_type: Type[WrappedType]) -> List[WrappedType]:
        """
        Wrap a list of root record models with a wrapper type.
        :param models list of wrapped record models, to unwrap
        :param wrapper_type the type to wrap these root models to.
        """
        return RecordModelWrapperUtil.wrap_list(models, wrapper_type)

    def _get_or_add_record(self, record: DataRecord):
        if record.get_record_id() in self.__record_by_record_id:
            return self.__record_by_record_id.get(record.get_record_id())
        record_model: PyRecordModel = PyRecordModel(record, self.record_model_manager)
        self.__known_records_by_type.put(record.get_data_type_name(), record_model)
        self.__record_by_record_id[record.get_record_id()] = record_model
        self.event_bus.fire_record_add_event(RecordAddedEvent(record_model))
        return record_model

    def _on_record_delete(self, model: PyRecordModel):
        """
        Internal method to fire on-delete events. Do not use.
        """
        if model.record_id in self.__record_by_record_id:
            del self.__record_by_record_id[model.record_id]
        self.__known_records_by_type.discard_value_from_all_keys(model)


class _InstanceRecordRollbackHandler(EventHandler[RollbackEvent]):
    _inst_man: RecordModelInstanceManager

    def __init__(self, inst_man: RecordModelInstanceManager):
        self._inst_man = inst_man

    def handle(self, event: RollbackEvent) -> None:
        # noinspection PyProtectedMember
        self._inst_man._on_rollback()


class _InstanceRecordCommitHandler(EventHandler[CommitEvent]):
    _inst_man: RecordModelInstanceManager

    def __init__(self, inst_man: RecordModelInstanceManager):
        self._inst_man = inst_man

    def handle(self, event: CommitEvent) -> None:
        # noinspection PyProtectedMember
        self._inst_man._on_commit()


class _InstanceRecordDeletedHandler(EventHandler[RecordDeletedEvent]):
    _inst_man: RecordModelInstanceManager

    def __init__(self, inst_man: RecordModelInstanceManager):
        self._inst_man = inst_man

    def handle(self, event: RecordDeletedEvent) -> None:
        # noinspection PyProtectedMember
        self._inst_man._on_record_delete(event.record)


class RecordModelRelationshipManager:
    """
    Manages parent-child relationships in record models.
    """
    _record_model_manager: RecordModelManager
    __instances: WeakValueDictionary[RecordModelManager, RecordModelRelationshipManager] = WeakValueDictionary()
    __initialized: bool

    def __new__(cls, record_model_manager: RecordModelManager):
        """
        Observes singleton pattern per record model manager object.
        """
        obj = cls.__instances.get(record_model_manager)
        if not obj:
            obj = object.__new__(cls)
            obj.__initialized = False
            cls.__instances[record_model_manager] = obj
        return obj

    def __init__(self, record_model_manager: RecordModelManager):
        if self.__initialized:
            return
        self._record_model_manager = record_model_manager
        self.__initialized = True

    def load_children_of_type(self, records: List[WrappedRecordModel], child_wrapped_type: Type[WrappedRecordModel]) \
            -> None:
        """
        Load children that we have not traversed yet.

        This call will not do anything to models that are deleted, models that are new,
        or models with children loaded already.
        """
        child_type_name: str = child_wrapped_type.get_wrapper_data_type_name()
        return self.load_children(RecordModelWrapperUtil.unwrap_list(records), child_type_name)

    def load_children(self, records: List[PyRecordModel], child_type_name: str) -> None:
        """
        Load children that we have not traversed yet.

        This call will not do anything to models that are deleted, models that are new,
        or models with children loaded already.
        """
        models_to_load: Set[PyRecordModel] = set()
        for record in records:
            if record.is_children_loaded(child_type_name):
                continue
            models_to_load.add(record)

        if not models_to_load:
            return

        from sapiopylib.rest.DataRecordManagerService import DataRecordManager
        from sapiopylib.rest.DataMgmtService import DataMgmtServer
        from sapiopylib.rest.pojo.DataRecordPaging import DataRecordPojoHierarchyListPageResult
        data_record_manager: DataRecordManager = DataMgmtServer.get_data_record_manager(self._record_model_manager.user)
        record_id_list_to_load: List[int] = [x.record_id for x in models_to_load]
        has_next_page: bool = True
        result_map: Dict[int, List[DataRecord]] = dict()
        while has_next_page:
            page_result: DataRecordPojoHierarchyListPageResult = data_record_manager.get_children_list(
                record_id_list_to_load, child_type_name)
            has_next_page = page_result.is_next_page_available
            result_map.update(page_result.result_map)
        inst_man = self._record_model_manager.instance_manager
        for source_record_id, children_record_list in result_map.items():
            source_model: PyRecordModel = inst_man.get_known_record_with_record_id(source_record_id)
            children_model_list: List[PyRecordModel] = inst_man.add_existing_records(children_record_list)
            source_model.mark_children_loaded(child_type_name, children_model_list)

    def load_parents_of_type(self, records: List[WrappedRecordModel], parent_wrapper_type: Type[WrappedRecordModel]) \
            -> None:
        """
        Load parents that we have not traversed yet.

        This call will not do anything to models that are deleted, models that are new,
        or models with parents loaded already.
        """
        return self.load_parents(RecordModelWrapperUtil.unwrap_list(records),
                                 parent_wrapper_type.get_wrapper_data_type_name())

    def load_parents(self, records: List[PyRecordModel], parent_type_name: str) -> None:
        """
        Load parents that we have not traversed yet.

        This call will not do anything to models that are deleted, models that are new,
        or models with parents loaded already.
        """
        models_to_load: Set[PyRecordModel] = set()
        for record in records:
            if record.is_parents_loaded(parent_type_name):
                continue
            models_to_load.add(record)

        if not models_to_load:
            return

        from sapiopylib.rest.DataRecordManagerService import DataRecordManager
        from sapiopylib.rest.DataMgmtService import DataMgmtServer
        from sapiopylib.rest.pojo.DataRecordPaging import DataRecordPojoHierarchyListPageResult
        data_record_manager: DataRecordManager = DataMgmtServer.get_data_record_manager(self._record_model_manager.user)
        record_id_list_to_load: List[int] = [x.record_id for x in models_to_load]
        has_next_page: bool = True
        result_map: Dict[int, List[DataRecord]] = dict()
        while has_next_page:
            page_result: DataRecordPojoHierarchyListPageResult = data_record_manager.get_parents_list(
                record_id_list_to_load, None, parent_type_name)
            has_next_page = page_result.is_next_page_available
            result_map.update(page_result.result_map)
        inst_man = self._record_model_manager.instance_manager
        for source_record_id, parent_record_list in result_map.items():
            source_model: PyRecordModel = inst_man.get_known_record_with_record_id(source_record_id)
            parent_model_list: List[PyRecordModel] = inst_man.add_existing_records(parent_record_list)
            source_model.mark_parents_loaded(parent_type_name, parent_model_list)

    def load_path(self, records: List[PyRecordModel], rel_path: RelationshipPath):
        """
        Load an entire path of records that we need to load along this path.
        If any parents or children for any records along this way are already loaded, it will not attempt to reload.
        """
        path: List[Tuple[RelationshipPathDir, str]] = rel_path.path
        cur_records: List[PyRecordModel] = records
        for direction, dt_name in path:
            next_records: List[PyRecordModel] = []
            if direction == RelationshipPathDir.PARENT:
                self.load_parents(cur_records, dt_name)
                for record in cur_records:
                    parents = record.get_parents_of_type(dt_name)
                    for parent in parents:
                        if parent not in next_records:
                            next_records.append(parent)
            elif direction == RelationshipPathDir.CHILD:
                self.load_children(cur_records, dt_name)
                for record in cur_records:
                    children = record.get_children_of_type(dt_name)
                    for child in children:
                        if child not in next_records:
                            next_records.append(child)
            else:
                raise ValueError("Unsupported direction: " + direction.name)
            cur_records = next_records


class RecordModelTransactionManager:
    """
    Holds the transaction properties for batch calls to Sapio server.
    """
    _record_model_manager: RecordModelManager
    __instances: WeakValueDictionary[RecordModelManager, RecordModelTransactionManager] = WeakValueDictionary()
    __initialized: bool
    _records_added: List[PyRecordModel]
    _records_deleted: List[PyRecordModel]
    _records_modified: Dict[PyRecordModel, Dict[str, Any]]
    _children_added: Set[Tuple[PyRecordModel, PyRecordModel]]
    _children_removed: Set[Tuple[PyRecordModel, PyRecordModel]]

    add_handler: _TransactionAddHandler
    delete_handler: _TransactionDeletedHandler
    field_change_handler: _TransactionFieldChangedHandler
    add_child_handler: _TransactionChildAddedHandler
    remove_child_handler: _TransactionChildRemovedHandler

    def __init__(self, record_model_manager: RecordModelManager):
        if self.__initialized:
            return
        self._record_model_manager = record_model_manager
        self._records_added = []
        self._records_deleted = []
        self._records_modified = dict()
        self._children_added = set()
        self._children_removed = set()
        self.add_handler = _TransactionAddHandler(self)
        self.event_bus.subscribe_record_add_event(self.add_handler)
        self.delete_handler = _TransactionDeletedHandler(self)
        self.event_bus.subscribe_record_delete_event(self.delete_handler)
        self.field_change_handler = _TransactionFieldChangedHandler(self)
        self.event_bus.subscribe_field_change_event(self.field_change_handler)
        self.add_child_handler = _TransactionChildAddedHandler(self)
        self.event_bus.subscribe_child_add_event(self.add_child_handler)
        self.remove_child_handler = _TransactionChildRemovedHandler(self)
        self.event_bus.subscribe_child_remove_event(self.remove_child_handler)
        self.__initialized = True

    def __new__(cls, record_model_manager: RecordModelManager):
        """
        Observes singleton pattern per record model manager object.
        """
        obj = cls.__instances.get(record_model_manager)
        if not obj:
            obj = object.__new__(cls)
            obj.__initialized = False
            cls.__instances[record_model_manager] = obj
        return obj

    def rollback(self) -> None:
        """
        Rollback all changes from record model cache without storing.
        """
        self._records_added.clear()
        self._records_deleted.clear()
        self._records_modified.clear()
        self._children_added.clear()
        self._children_removed.clear()
        self.event_bus.fire_rollback_event()

    def commit(self) -> None:
        """
        Store and commit the current changes of record model to Sapio Platform.
        These changes will become permanent.

        New records with temporary negative record IDs will be reassigned with new positive and permanent record IDs.
        """
        records_added: List[DataRecord] = []
        for model_added in self._records_added:
            decorated = DataRecord(model_added.data_type_name, model_added.record_id,
                                   model_added.fields.copy_to_dict())
            records_added.append(decorated)

        records_deleted: List[DataRecordDescriptor] = []
        for model_deleted in self._records_deleted:
            if model_deleted.is_new:
                continue
            decorated = DataRecordDescriptor(model_deleted.data_type_name, model_deleted.record_id)
            records_deleted.append(decorated)

        record_field_changes: List[DataRecord] = []
        for model_changed in self._records_modified:
            decorated = DataRecord(model_changed.data_type_name, model_changed.record_id,
                                   model_changed.fields.copy_to_dict())
            record_field_changes.append(decorated)

        child_records_added: List[DataRecordRelationChangePojo] = []
        for parent, child in self._children_added:
            parent_desc = DataRecordDescriptor(parent.data_type_name, parent.record_id)
            child_desc = DataRecordDescriptor(child.data_type_name, child.record_id)
            child_records_added.append(DataRecordRelationChangePojo(parent_desc, child_desc))

        child_records_removed: List[DataRecordRelationChangePojo] = []
        for parent, child in self._children_removed:
            parent_desc = DataRecordDescriptor(parent.data_type_name, parent.record_id)
            child_desc = DataRecordDescriptor(child.data_type_name, child.record_id)
            child_records_removed.append(DataRecordRelationChangePojo(parent_desc, child_desc))

        updater = DataRecordBatchUpdate(records_added=records_added, records_deleted=records_deleted,
                                        records_fields_changed=record_field_changes,
                                        child_links_added=child_records_added,
                                        child_links_removed=child_records_removed)

        sub_path = '/datarecordlist/runbatchupdate'
        payload = updater.to_json()
        response = self._record_model_manager.user.post(sub_path, payload=payload)
        self._record_model_manager.user.raise_for_status(response)
        json_dict = response.json()

        refreshed_data: DataRecordBatchResult = DataRecordBatchResult.from_json(json_dict)
        record_updates: Dict[int, DataRecordDescriptor] = refreshed_data.added_record_updates
        inst_man: RecordModelInstanceManager = self._record_model_manager.instance_manager
        for temp_record_id, desc in record_updates.items():
            model: PyRecordModel = inst_man.get_known_record_with_record_id(temp_record_id)
            if model is not None:
                model.record_id = desc.record_id
        self.event_bus.fire_commit_event()

    @property
    def event_bus(self) -> RecordModelEventBus:
        return self._record_model_manager.event_bus

    def _add_field_change(self, record: PyRecordModel, field_name: str, field_value: Any):
        """
        Internal method to handle field change events. Do not use.
        """
        if record.is_new:
            return
        if record not in self._records_modified:
            self._records_modified[record] = dict()
        field_map: Dict[str, Any] = self._records_modified[record]
        field_map[field_name] = field_value

    def _on_record_delete(self, record_to_delete: PyRecordModel):
        """
        Internal method to handle record delete events. Do not use.
        """
        if record_to_delete.is_new:
            self._records_added.remove(record_to_delete)
        else:
            self._records_deleted.append(record_to_delete)
        for parent, child in self._children_added.copy():
            if parent == record_to_delete:
                self._children_added.discard((parent, child))
            if child == record_to_delete:
                self._children_added.discard((parent, child))
        for parent, child in self._children_removed.copy():
            if parent == record_to_delete:
                self._children_removed.discard((parent, child))
            if child == record_to_delete:
                self._children_removed.discard((parent, child))

    def _on_record_add(self, record_to_add: PyRecordModel):
        """
        Internal method to handle record-add events. Do not use.
        """
        if record_to_add.is_new:
            self._records_added.append(record_to_add)

    def _on_child_add(self, parent_record: PyRecordModel, child_record: PyRecordModel):
        """
        Internal method to handle child-add events. Do not use.
        """
        if parent_record.is_deleted or child_record.is_deleted:
            return
        self._children_added.add((parent_record, child_record))

    def _on_child_remove(self, parent_record: PyRecordModel, child_record: PyRecordModel):
        """
        Internal method to handle child-remove events. Do not use.
        """
        if parent_record.is_deleted or child_record.is_deleted:
            return
        if (parent_record, child_record) in self._children_added:
            self._children_added.discard((parent_record, child_record))
        else:
            self._children_removed.add((parent_record, child_record))


class _TransactionChildAddedHandler(EventHandler[ChildAddedEvent]):
    _trans_man: RecordModelTransactionManager

    def __init__(self, trans_man: RecordModelTransactionManager):
        self._trans_man = trans_man

    def handle(self, event: ChildAddedEvent) -> None:
        # noinspection PyProtectedMember
        self._trans_man._on_child_add(event.parent, event.child)


class _TransactionChildRemovedHandler(EventHandler[ChildRemovedEvent]):
    _trans_man: RecordModelTransactionManager

    def __init__(self, trans_man: RecordModelTransactionManager):
        self._trans_man = trans_man

    def handle(self, event: ChildRemovedEvent) -> None:
        # noinspection PyProtectedMember
        self._trans_man._on_child_remove(event.parent, event.child)


class _TransactionFieldChangedHandler(EventHandler[FieldChangeEvent]):
    _trans_man: RecordModelTransactionManager

    def __init__(self, trans_man: RecordModelTransactionManager):
        self._trans_man = trans_man

    def handle(self, event: FieldChangeEvent) -> None:
        record = event.record
        field_name = event.field_name
        new_value = event.new_value
        self._trans_man._add_field_change(record, field_name, new_value)


class _TransactionDeletedHandler(EventHandler[RecordDeletedEvent]):
    _trans_man: RecordModelTransactionManager

    def __init__(self, trans_man: RecordModelTransactionManager):
        self._trans_man = trans_man

    def handle(self, event: RecordDeletedEvent) -> None:
        # noinspection PyProtectedMember
        self._trans_man._on_record_delete(event.record)


class _TransactionAddHandler(EventHandler[RecordAddedEvent]):
    _trans_man: RecordModelTransactionManager

    def __init__(self, trans_man: RecordModelTransactionManager):
        self._trans_man = trans_man

    def handle(self, event: RecordAddedEvent) -> None:
        # noinspection PyProtectedMember
        self._trans_man._on_record_add(event.record)
