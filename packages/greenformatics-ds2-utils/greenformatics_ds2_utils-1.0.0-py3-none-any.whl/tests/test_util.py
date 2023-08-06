# coding=utf-8

import unittest
from greenformatics_ds2_utils import ClassLoader
from tests import TestClass


class UtilityTestCase(unittest.TestCase):

    def test_class_loader(self):
        actual = ClassLoader.load('tests', 'TestClass', 31, 'Marketing')  # type: TestClass
        self.assertIsInstance(actual, TestClass)
        self.assertEqual(actual.id, 31)
        self.assertEqual(actual.name, 'Marketing')
        self.assertIsNone(actual.description)
