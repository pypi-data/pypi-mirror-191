from __future__ import annotations

from typing import List, Any, Dict, Set, Optional

from sapiopylib.rest.pojo.DataRecord import DataRecord
from sapiopylib.rest.utils.MultiMap import SetMultimap


class SapioRecordModelException(Exception):
    """
    This error will be thrown when record model encountered an error while using.
    """
    msg: str
    model: PyRecordModel

    def __init__(self, msg: str, model: PyRecordModel):
        self.msg = msg
        self.model = model

    def __str__(self):
        return "Record Model with Record ID " + str(self.model.record_id) + ": " + self.msg


class RecordModelFieldMap:
    """
    Provides record model field map supports.

    This class provides proper views for current state of record model data in a dictionary-like access structure.

    It will also provide fire record model events when any field values are changed.

    This class supports random access. For example py_model.fields[field_name]=field_value
    """
    _model: PyRecordModel
    _model_fields: Dict[str, Any]

    def __init__(self, model: PyRecordModel, model_fields: Dict[str, Any] = None):
        self._model = model
        # Always make a copy and always be non-trivial.
        if model_fields is None:
            model_fields = dict()
        else:
            model_fields = dict(model_fields)
        self._model_fields = model_fields

    def __getitem__(self, field_name: str):
        return self._model_fields.__getitem__(field_name)

    def get(self, field_name: str):
        """
        Get the value by a field name in this record model.
        Return None if this field does not exist.
        """
        return self._model_fields.get(field_name)

    def __setitem__(self, field_name: str, field_value: Any):
        old_value = self._model_fields.get(field_name)
        if old_value == field_value:
            return
        self._model_fields[field_name] = field_value
        from sapiopylib.rest.utils.recordmodel.RecordModelEvents import FieldChangeEvent
        self._model.record_model_manager.event_bus.fire_field_change_event(FieldChangeEvent(
            self._model, field_name, old_value, field_value))

    def __delitem__(self, field_name: str):
        if field_name not in self._model_fields:
            return
        old_value = self._model_fields.get(field_name)
        del self._model_fields[field_name]
        from sapiopylib.rest.utils.recordmodel.RecordModelEvents import FieldChangeEvent
        self._model.record_model_manager.event_bus.fire_field_change_event(FieldChangeEvent(
            self._model, field_name, old_value, None))

    def __hash__(self):
        return hash((self._model, self._model_fields))

    def __eq__(self, other):
        if not isinstance(other, RecordModelFieldMap):
            return False
        return self._model == other._model and self._model_fields == other._model_fields

    def __str__(self):
        return str(self._model_fields)

    def __iter__(self):
        return self._model_fields.__iter__()

    def items(self):
        """
        Return a set-like object with tuples in iterator.
        """
        return self._model_fields.items()

    def copy_to_dict(self):
        """
        Copy current state of the data into a dictionary. The copy will not modify the current record model's state.
        """
        return dict(self._model_fields)


class PyRecordModel:
    """
    A record model instance that is backed by a data record.
    """
    _backing_record: DataRecord
    _model_fields: RecordModelFieldMap
    __is_deleted: bool

    _children_types_loaded: Set[str]
    _parent_types_loaded: Set[str]
    _children_models_by_type: SetMultimap[str, PyRecordModel]
    _parent_models_by_type: SetMultimap[str, PyRecordModel]

    _removed_parents: Set[PyRecordModel]
    _removed_children: Set[PyRecordModel]

    def __str__(self):
        return self.data_type_name + " " + str(self.record_id) + ": " + str(self.fields)

    def __init__(self, backing_record: DataRecord, record_model_manager):
        self._backing_record = backing_record
        self._model_fields = RecordModelFieldMap(self, backing_record.get_fields())
        self._record_model_manager = record_model_manager
        self.__is_deleted = False
        self._children_types_loaded = set()
        self._parent_types_loaded = set()
        self._children_models_by_type = SetMultimap()
        self._parent_models_by_type = SetMultimap()
        self._removed_parents = set()
        self._removed_children = set()

    def __hash__(self):
        return self._backing_record.__hash__()

    def __eq__(self, other):
        if not isinstance(other, PyRecordModel):
            return False
        return self._backing_record.__eq__(other._backing_record)

    @property
    def record_id(self) -> int:
        """
        The record ID of the current model.
        It is possible for this number to be negative, if it is a new record.
        """
        return self._backing_record.record_id

    @record_id.setter
    def record_id(self, record_id: int) -> None:
        """
        Record ID on record model will be reset when the added record is now living permanently in Sapio DB.
        """
        if self.record_id >= 0:
            raise SapioRecordModelException('Cannot replace record ID when the current ID is non-negative.', self)
        self._backing_record.record_id = record_id

    @property
    def is_deleted(self) -> bool:
        """
        Test whether this record is flagged for deletion.
        """
        return self.__is_deleted

    @property
    def is_new(self) -> bool:
        """
        Tests whether this is a new record that has not been stored in Sapio yet.
        """
        return self._backing_record.get_record_id() < 0

    @property
    def fields(self) -> RecordModelFieldMap:
        """
        The field map of the record model, which could include cached changed not committed to data record.
        """
        return self._model_fields

    @property
    def data_type_name(self) -> str:
        """
        The data type name of this record model.
        """
        return self._backing_record.get_data_type_name()

    def is_children_loaded(self, child_type_name: str) -> bool:
        """
        Tests whether the children for this model has been loaded already.
        """
        return self.is_deleted or self.is_new or (child_type_name in self._children_types_loaded)

    def is_parents_loaded(self, parent_type_name: str) -> bool:
        """
        Tests whether the parents for this model has been loaded already.
        """
        return self.is_deleted or self.is_new or (parent_type_name in self._parent_types_loaded)

    def mark_children_loaded(self, child_type_name: str, children_loaded: List[PyRecordModel]) -> None:
        """
        When record model management finishes loading children for this instance, it calls this method to update the
        children list.

        This is an internal method for record model.
        :param child_type_name: The child type for which we have just loaded for this instance.
        :param children_loaded: The loaded children record models for this instance.
        """
        self._children_types_loaded.add(child_type_name)
        for child in children_loaded:
            if child in self._removed_children:
                continue
            self._children_models_by_type.put(child_type_name, child)

    def mark_parents_loaded(self, parent_type_name: str, parents_loaded: List[PyRecordModel]) -> None:
        """
        When record model management finishes loading parents for this instance, it calls this method to update the
        parents list.

        This is an internal method for record model.
        :param parent_type_name: The parent type for which we have just loaded for this instance.
        :param parents_loaded: The loaded parent record models for this instance.
        """
        self._parent_types_loaded.add(parent_type_name)
        for parent in parents_loaded:
            if parent in self._removed_parents:
                continue
            self._parent_models_by_type.put(parent_type_name, parent)

    def get_field_value(self, field_name: str) -> Any:
        """
        Get the model's field value for a field
        """
        return self._model_fields.get(field_name)

    def get_record_field_value(self, field_name: str) -> Any:
        """
        Get the backing record's field value for a field.
        """
        return self._backing_record.get_field_value(field_name)

    def get_data_record(self) -> DataRecord:
        """
        Get the backing data record for this record model instance.
        """
        return self._backing_record

    def add_parent(self, parent_record: PyRecordModel, fire_events: bool = True) -> None:
        """
        Add a record model as a parent for this record model.
        """
        self._parent_models_by_type.put(parent_record.data_type_name, parent_record)
        if fire_events:
            parent_record.add_child(self, fire_events=False)
            from sapiopylib.rest.utils.recordmodel.RecordModelEvents import ChildAddedEvent
            self._record_model_manager.event_bus.fire_child_add_event(ChildAddedEvent(parent_record, self))

    def add_parents(self, parent_records: List[PyRecordModel]) -> None:
        """
        Add multiple record models as parents for this record model.
        """
        for parent_record in parent_records:
            self.add_parent(parent_record)

    def remove_parent(self, parent_record: PyRecordModel, fire_events: bool = True) -> None:
        """
        Remove a parent relation from this record model.
        """
        self._parent_models_by_type.get(parent_record.data_type_name).discard(parent_record)
        self._removed_parents.add(parent_record)
        if fire_events:
            parent_record.remove_child(self, fire_events=False)
            from sapiopylib.rest.utils.recordmodel.RecordModelEvents import ChildRemovedEvent
            self._record_model_manager.event_bus.fire_child_remove_event(ChildRemovedEvent(parent_record, self))

    def remove_parents(self, parent_records: List[PyRecordModel]) -> None:
        """
        Remove multiple parent relations from this record model.
        """
        for parent_record in parent_records:
            self.remove_parent(parent_record)

    def add_child(self, child_record: PyRecordModel, fire_events: bool = True) -> None:
        """
        Add a child record model for this record model.
        """
        self._children_models_by_type.put(child_record.data_type_name, child_record)
        if fire_events:
            child_record.add_parent(self, fire_events=False)
            from sapiopylib.rest.utils.recordmodel.RecordModelEvents import ChildAddedEvent
            self._record_model_manager.event_bus.fire_child_add_event(ChildAddedEvent(self, child_record))

    def add_children(self, children_records: List[PyRecordModel]) -> None:
        """
        Add multiple children record model for this record model.
        """
        for child_record in children_records:
            self.add_child(child_record)

    def remove_child(self, child_record: PyRecordModel, fire_events: bool = True) -> None:
        """
        Remove a child record model relation from this record model.
        """
        self._removed_children.add(child_record)
        self._children_models_by_type.get(child_record.data_type_name).discard(child_record)
        if fire_events:
            child_record.remove_parent(self, fire_events=False)
            from sapiopylib.rest.utils.recordmodel.RecordModelEvents import ChildRemovedEvent
            self._record_model_manager.event_bus.fire_child_remove_event(ChildRemovedEvent(self, child_record))

    def remove_children(self, children_records: List[PyRecordModel]) -> None:
        """
        Remove multiple children record model relations from this record model.
        """
        for child_record in children_records:
            self.remove_child(child_record)

    def delete(self) -> None:
        """
        Flag the current record model to be deleted on commit.
        """
        from sapiopylib.rest.utils.recordmodel.RecordModelEvents import RecordDeletedEvent
        self._record_model_manager.event_bus.fire_record_delete_event(RecordDeletedEvent(self))

    def set_field_value(self, field_name: str, field_value: Any) -> None:
        """
        Set a current record model's field value to a new value.
        """
        self._model_fields[field_name] = field_value

    def set_field_values(self, field_change_map: Dict[str, Any]) -> None:
        """
        Set multiple field values for this record model to new values.
        """
        for key, value in field_change_map.items():
            self.set_field_value(key, value)

    def get_parents_of_type(self, parent_type_name: str) -> List[PyRecordModel]:
        """
        Get all parents for a particular data type name for this record model.
        """
        if not self.is_parents_loaded(parent_type_name):
            raise SapioRecordModelException("Parent type " + parent_type_name + " was not loaded.", self)
        return list(self._parent_models_by_type.get(parent_type_name))

    def get_children_of_type(self, child_type_name: str) -> List[PyRecordModel]:
        """
        Get all children for a particular data type name for this record model.
        """
        if not self.is_children_loaded(child_type_name):
            raise SapioRecordModelException("Child type " + child_type_name + " was not loaded.", self)
        return list(self._children_models_by_type.get(child_type_name))

    def get_parent_of_type(self, parent_type_name: str) -> Optional[PyRecordModel]:
        """
        Obtains the parent of the current record of the provided data type name.
        If the parent is not found, return None.
        If there are more than one parent exists, then we will throw an exception.
        """
        parents = self.get_parents_of_type(parent_type_name)
        if not parents:
            return None
        if len(parents) > 1:
            raise SapioRecordModelException("Too many parent records of type " + parent_type_name, self)
        return parents[0]

    def get_child_of_type(self, child_type_name: str) -> Optional[PyRecordModel]:
        """
        Obtains the only child of the current record of the provided data type name.
        If the child is not found, return None.
        If there are more than one child exists, then we will throw an exception.
        """
        children = self.get_children_of_type(child_type_name)
        if not children:
            return None
        if len(children) > 1:
            raise SapioRecordModelException("Too many child records of type " + child_type_name, self)
        return children[0]

    def do_rollback(self):
        """
        This method is called by instance manager for referencable record models when a rollback event is fired.
        This is an internal method.
        """
        self.__is_deleted = False
        self._model_fields = RecordModelFieldMap(self, self._backing_record.fields)
        self._removed_parents.clear()
        self._removed_children.clear()
        self._children_types_loaded.clear()
        self._parent_types_loaded.clear()
        self._children_models_by_type.clear()
        self._parent_models_by_type.clear()

    def do_commit(self):
        """
        This method is called by instance manager for referencable record models when a commit event is fired.
        This is an internal method.
        """
        if self.__is_deleted:
            return
        self._backing_record.set_fields(self.fields.copy_to_dict())
        self._backing_record.commit_changes()

    @property
    def record_model_manager(self):
        return self._record_model_manager
