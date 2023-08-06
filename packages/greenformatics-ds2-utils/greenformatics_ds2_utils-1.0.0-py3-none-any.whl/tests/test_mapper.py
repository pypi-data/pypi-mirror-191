# coding=utf-8

from unittest import TestCase
from greenformatics_ds2_utils.mapper import *
from greenformatics_ds2_utils.converter import camel_case_to_snake_case, nfkd_normalized_lower_no_spec
from tests import TestClass, TestClass2


class MapperUtilityTestCase(TestCase):

    def test_dict_to_object_mapper(self):
        data = {'Id': 31, 'Name': 'Marketing', 'Foo': 'Bar'}
        attr_name_map = {'Foo': 'Description'}
        mapped_object = map_dict_to_object(data, TestClass, camel_case_to_snake_case, attr_name_map)
        self.assertEqual(mapped_object.id, 31)
        self.assertEqual(mapped_object.name, 'Marketing')
        self.assertEqual(mapped_object.description, 'Bar')

        data = {'Id': 31, 'Name': [], 'Foo': {}}
        mapped_object = map_dict_to_object(data, TestClass, camel_case_to_snake_case, attr_name_map)
        self.assertEqual(mapped_object.id, 31)
        self.assertEqual(mapped_object.name, '[]')
        self.assertEqual(mapped_object.description, '{}')

    def test_dict_to_entity_mapping(self):
        data = {'Id': 31, 'Name': 'Marketing'}
        mapped_object = dict_to_object_in_snake_case(data, TestClass)
        self.assertEqual(mapped_object.id, 31)
        self.assertEqual(mapped_object.name, 'Marketing')
        data = {'Id': 31, 'Name': 'Marketing', 'Foo': 'Bar'}
        attr_name_map = {'Foo': 'Description'}
        mapped_object = dict_to_object_in_snake_case(data, TestClass, attr_name_map)
        self.assertEqual(mapped_object.id, 31)
        self.assertEqual(mapped_object.name, 'Marketing')
        self.assertEqual(mapped_object.description, 'Bar')

    def test_dict_list_to_entity_list_mapping(self):
        data_list = [{'Id': 31, 'Name': 'Marketing'},
                     {'Id': 26, 'Name': 'Sales'}]
        entities = dict_list_to_object_list(data_list, TestClass)
        self.assertEqual(len(entities), 2)
        self.assertIsInstance(entities[0], TestClass)
        self.assertEqual(entities[0].id, 31)
        self.assertEqual(entities[0].name, 'Marketing')
        self.assertIsInstance(entities[1], TestClass)
        self.assertEqual(entities[1].id, 26)
        self.assertEqual(entities[1].name, 'Sales')

        attr_name_map = {'Foo': 'Description'}
        data_list = [{'Id': 31, 'Name': 'Marketing', 'Foo': 'Bar'},
                     {'Id': 26, 'Name': 'Sales', 'Foo': 'Fighters'}]
        entities = dict_list_to_object_list(data_list, TestClass, nfkd_normalized_lower_no_spec, attr_name_map)
        self.assertEqual(len(entities), 2)
        self.assertIsInstance(entities[0], TestClass)
        self.assertEqual(entities[0].id, 31)
        self.assertEqual(entities[0].name, 'Marketing')
        self.assertEqual(entities[0].description, 'Bar')
        self.assertIsInstance(entities[1], TestClass)
        self.assertEqual(entities[1].id, 26)
        self.assertEqual(entities[1].name, 'Sales')
        self.assertEqual(entities[1].description, 'Fighters')

    def test_embedded_object_and_list(self):
        data_list = [{'Id': 3649, 'UserId': 'Adam', 'AddressId': 1, 'Attachments': [], 'Members': [], 'Notes': []},
                     {'Id': 4461, 'UserId': 'Peter', 'Attachments': [], 'Members': [], 'Notes': {}}]
        entities = dict_list_to_object_list(data_list, TestClass2, nfkd_normalized_lower_no_spec)
        self.assertEqual(len(entities), 2)
        entity = entities[0]  # type: TestClass2
        self.assertIsInstance(entity, TestClass2)
        self.assertEqual(entity.id, 3649)
        self.assertEqual(entity.userid, 'Adam')
        self.assertEqual(entity.addressid, 1)
        self.assertEqual(entity.attachments, '[]')
        self.assertEqual(entity.members, '[]')
        self.assertEqual(entity.notes, '[]')
        entity = entities[1]  # type: TestClass2
        self.assertIsInstance(entity, TestClass2)
        self.assertEqual(entity.id, 4461)
        self.assertEqual(entity.userid, 'Peter')
        self.assertEqual(entity.addressid, None)
        self.assertEqual(entity.attachments, '[]')
        self.assertEqual(entity.members, '[]')
        self.assertEqual(entity.notes, '{}')

    def test_dict_to_object_in_lower_case_db_safe(self):
        data = {'Id': 3649, 'UserId': 'Ádám', 'AddressId': 0, 'Members': [], 'Notes': {}}
        entity = dict_to_object_in_lower_case_db_safe(data, TestClass2)  # type: TestClass2
        self.assertIsInstance(entity, TestClass2)
        self.assertEqual(entity.id, 3649)
        self.assertEqual(entity.userid, 'Ádám')
        self.assertEqual(entity.addressid, 0)
        self.assertEqual(entity.attachments, None)
        self.assertEqual(entity.members, '[]')
        self.assertEqual(entity.notes, '{}')
