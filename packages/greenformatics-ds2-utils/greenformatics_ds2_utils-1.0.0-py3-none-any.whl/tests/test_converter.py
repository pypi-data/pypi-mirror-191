# coding=utf-8

from unittest import TestCase
from greenformatics_ds2_utils.converter import *


class MapperUtilityTestCase(TestCase):
    def test_camel_to_snake(self):
        expected = 'id'
        actual = camel_case_to_snake_case('Id')
        self.assertEqual(actual, expected)
        expected = 'some_name'
        actual = camel_case_to_snake_case('Some_Name')
        self.assertEqual(actual, expected)
        actual = camel_case_to_snake_case(None)
        self.assertIsNone(actual)

    def test_nfkd_normalized(self):
        expected = 'aaAbceEiIoOoOoOuUuUuUaA'
        actual = nfkd_normalized('aáÁbcéÉíÍóÓöÖőŐúÚüÜűŰäÄ')
        self.assertEqual(expected, actual)
        actual = nfkd_normalized(None)
        self.assertIsNone(actual)

    def test_nfkd_normalized_lower(self):
        expected = 'aaabceeiioooooouuuuuuaa'
        actual = nfkd_normalized_lower('aáÁbcéÉíÍóÓöÖőŐúÚüÜűŰäÄ')
        self.assertEqual(expected, actual)
        actual = nfkd_normalized_lower(None)
        self.assertIsNone(actual)

    def test_nfkd_normalized_lower_no_spec(self):
        expected = 'aaabceeiioooooouuuuuuaa'
        actual = nfkd_normalized_lower_no_spec('_aá_Ábcé_ÉíÍóÓöÖőŐúÚüÜűŰäÄ_')
        self.assertEqual(expected, actual)
        actual = nfkd_normalized_lower_no_spec(None)
        self.assertIsNone(actual)

    def test_nfkd_normalized_lower_db_safe(self):
        expected = '_aa_abce_eiioooooouuuuuuaa_'
        actual = nfkd_normalized_lower_db_safe('_aá_Ábcé_ÉíÍóÓöÖőŐúÚüÜűŰäÄ_')
        self.assertEqual(expected, actual)
        actual = nfkd_normalized_lower_db_safe(None)
        self.assertIsNone(actual)

    def test_empty_str_to_none(self):
        self.assertIsNone(empty_str_to_none(' '))
        self.assertIsNone(empty_str_to_none(''))
        self.assertEqual(' A ', empty_str_to_none(' A '))
        self.assertIsNone(empty_str_to_none(None))

    def test_missing_key(self):
        attribute_map = {'primary_key': 'id'}
        self.assertEqual(map_attribute_name(attribute_map, 'primary_key'), 'id')
        self.assertEqual(map_attribute_name(attribute_map, 'some_key'), 'some_key')
        self.assertEqual(map_attribute_name(None, 'some_key'), 'some_key')

    def test_year_zero_to_none(self):
        self.assertIsNone(year_zero_to_none('0000-00-00 00:00:00'))
        self.assertIsNotNone(year_zero_to_none('2023-01-01 00:00:00'))
        self.assertIsNone(year_zero_to_none('0000-00-00'))
        self.assertIsNotNone(year_zero_to_none('2023-01-01'))
        self.assertIsNone(year_zero_to_none(None))
