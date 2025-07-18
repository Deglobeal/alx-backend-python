#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_utils.py
Unit tests for utility functions in the project.
parameterize a usint test function to run it with different inputs.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map



class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test accessing nested maps with various paths.
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)