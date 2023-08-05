from __future__ import annotations

from typing import Dict, List, Any
from weakref import WeakValueDictionary

from sapiopylib.rest.pojo.datatype.FieldDefinition import AbstractVeloxFieldDefinition
from sapiopylib.rest.DataTypeService import DataTypeManager
from sapiopylib.rest.pojo.datatype.DataType import DataTypeDefinition
from sapiopylib.rest.User import SapioUser


class DataTypeCacheManager:
    """
    Manages a data type cache for the purpose retrieving data type and data field definitions efficiently.
    """
    user: SapioUser
    __instances: WeakValueDictionary[SapioUser, DataTypeCacheManager] = WeakValueDictionary()
    __initialized: bool
    __data_type_cache: Dict[str, DataTypeDefinition]
    __data_field_cache: Dict[str, List[AbstractVeloxFieldDefinition]]

    def __new__(cls, user: SapioUser):
        """
        Observes singleton pattern per record model manager object.
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
        self.user = user
        self.__data_type_cache = dict()
        self.__data_field_cache = dict()
        self.__initialized = True

    def get_display_name(self, dt_name: str) -> str:
        """
        Retrieve the display name of a data type.
        """
        return self.get_data_type(dt_name).display_name

    def get_plural_display_name(self, dt_name: str) -> str:
        """
        Retrieve the plural display name of a data type.
        """
        return self.get_data_type(dt_name).plural_display_name

    def get_default_field_map(self, dt_name: str) -> Dict[str, Any]:
        """
        Obtain the default value field map for a data type.
        This will not include any field names whose default value is blank.
        """
        field_list: List[AbstractVeloxFieldDefinition] = self.get_fields_for_type(dt_name)
        ret: Dict[str, Any] = dict()
        for field in field_list:
            field_name = field.get_data_field_name()
            if hasattr(field, 'default_value'):
                default_value: Any = getattr(field, 'default_value')
                if default_value:
                    ret[field_name] = default_value
        return ret

    def get_data_type(self, dt_name: str) -> DataTypeDefinition:
        """
        Retrieve the data type definition object from cache.
        If this cache is not loaded, load it right now.
        """
        if dt_name in self.__data_type_cache:
            return self.__data_type_cache[dt_name]
        dt_man: DataTypeManager = DataTypeManager(self.user)
        dt_def: DataTypeDefinition = dt_man.get_data_type_definition(dt_name)
        self.__data_type_cache[dt_name] = dt_def
        return dt_def

    def get_fields_for_type(self, dt_name: str) -> List[AbstractVeloxFieldDefinition]:
        """
        Retrieve the data field definitions for a data type from cache.
        If this is not loaded, load it right now.
        """
        if dt_name in self.__data_field_cache:
            return self.__data_field_cache[dt_name]
        dt_man: DataTypeManager = DataTypeManager(self.user)
        field_list = dt_man.get_field_definition_list(dt_name)
        self.__data_field_cache[dt_name] = field_list
        return field_list

