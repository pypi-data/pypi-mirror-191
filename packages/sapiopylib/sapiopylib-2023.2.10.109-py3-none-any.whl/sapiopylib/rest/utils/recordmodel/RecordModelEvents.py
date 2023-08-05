from typing import Any

from buslane.events import Event

from sapiopylib.rest.utils.recordmodel.PyRecordModel import PyRecordModel


class ChildAddedEvent(Event):
    """
    This event is fired when a new parent-child relationship is added through record model.
    """
    __parent: PyRecordModel
    __child: PyRecordModel

    def __init__(self, parent: PyRecordModel, child: PyRecordModel):
        self.__parent = parent
        self.__child = child

    @property
    def parent(self) -> PyRecordModel:
        return self.__parent

    @property
    def child(self) -> PyRecordModel:
        return self.__child


class ChildRemovedEvent(Event):
    """
    This event is fired when an existing parent-child relationship is removed through record model.
    """
    __parent: PyRecordModel
    __child: PyRecordModel

    def __init__(self, parent: PyRecordModel, child: PyRecordModel):
        self.__parent = parent
        self.__child = child

    @property
    def parent(self) -> PyRecordModel:
        return self.__parent

    @property
    def child(self) -> PyRecordModel:
        return self.__child


class FieldChangeEvent(Event):
    """
    This event is fired when a data field value is changed through record model.
    """
    __record: PyRecordModel
    __field_name: str
    __old_value: Any
    __new_value: Any

    def __init__(self, record: PyRecordModel, field_name: str, old_value: Any, new_value: Any):
        self.__record = record
        self.__field_name = field_name
        self.__old_value = old_value
        self.__new_value = new_value

    @property
    def record(self) -> PyRecordModel:
        return self.__record

    @property
    def field_name(self) -> str:
        return self.__field_name

    @property
    def old_value(self) -> Any:
        return self.__old_value

    @property
    def new_value(self) -> Any:
        return self.__new_value


class RecordAddedEvent(Event):
    """
    This event is fired when a new data record is added through record model.
    """
    __record: PyRecordModel

    def __init__(self, record: PyRecordModel):
        self.__record = record

    @property
    def record(self) -> PyRecordModel:
        return self.__record


class RecordDeletedEvent(Event):
    """
    This event is fired when an existing record is deleted through record model.
    """
    __record: PyRecordModel

    def __init__(self, record: PyRecordModel):
        self.__record = record

    @property
    def record(self) -> PyRecordModel:
        return self.__record


class RollbackEvent(Event):
    """
    This event is fired when rollback happens from transaction manager.
    """


class CommitEvent(Event):
    """
    This event is fired when rollback happens from transaction manager.
    """
