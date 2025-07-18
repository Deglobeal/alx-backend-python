#!/usr/bin/env python3
import unittest
from parameterized import parameterized

from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Unit test for access_nested_map"""

    @parameterized.expand([
        ("simple_map", {"a": 1}, ("a",), 1),
        ("nested_map_level_1", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("nested_map_level_2", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test access_nested_map with various paths"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
