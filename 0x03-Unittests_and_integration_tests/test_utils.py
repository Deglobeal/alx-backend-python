#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function"""

    @parameterized.expand([
        ("key_missing_in_empty_map", {}, ("a",), "'a'"),
        ("key_missing_in_nested_path", {"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path, expected_message):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)
