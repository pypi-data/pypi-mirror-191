# coding=utf-8

import abc
import sys


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class ClassLoader:
    @classmethod
    def load(cls, module_name, class_name, *args):
        __import__(module_name)
        module_ = sys.modules[module_name]
        return getattr(module_, class_name)(*args)


class APIObjectRetrieverServiceInterface(metaclass=abc.ABCMeta):

    _API_OBJECT_NAME = ''

    def __init__(self, endpoint=None, filtering_params=None):
        # Set the network endpoint where the data to be retrieved from
        self._endpoint = f"{endpoint}{self._API_OBJECT_NAME}"
        # Set filtering criteria to be applied while query the data
        self._filtering_params = filtering_params

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'retrieve_entity_ids') and
                callable(subclass.retrieve_entity_ids) and
                hasattr(subclass, 'retrieve_entity') and
                callable(subclass.retrieve_entity) and
                hasattr(subclass, 'get_entity_dict_list') and
                callable(subclass.get_entity_dict_list) and
                hasattr(subclass, 'run_scraping') and
                callable(subclass.run_scraping) or
                NotImplemented)

    @abc.abstractmethod
    def _retrieve_entity_ids(self):
        """Retrieve the list of IDs from the API"""

        raise NotImplementedError

    @abc.abstractmethod
    def _retrieve_entity(self, object_id: str):
        """Retrieve the entity details by its ID"""

        raise NotImplementedError

    @abc.abstractmethod
    def _get_entity_dict_list(self):
        """Create a list of dictionaries containing the detailed data of the API object"""

        raise NotImplementedError

    @abc.abstractmethod
    def run_scraping(self):
        """Orchestrates the API data retrieving of a given API object"""

        raise NotImplementedError


class APIObjectStoringRepositoryInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'map_data_to_dao') and
                callable(subclass.map_data_to_dao) and
                hasattr(subclass, 'bulk_insert_entities') and
                callable(subclass.bulk_insert_entities) or
                NotImplemented)

    @abc.abstractmethod
    def _map_data_to_dao(self):
        """Maps the list of data dictionary retrieved from API ot DAO"""

        raise NotImplementedError

    def bulk_insert_entities(self):
        # Map the JSON response transformed to dictionary to DAO
        entity_list = self._map_data_to_dao()
        self._session.bulk_save_objects(entity_list)
        # We won't commit here as the whole service run should be in one database transaction

