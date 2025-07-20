#!/usr/bin/env python3
"""Unit tests for utility functions."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
            self, nested_map, path, expected_message):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(
            str(context.exception),
            expected_message
        )


class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(
            test_url
        )
        self.assertEqual(
            result,
            test_payload
        )
        def test_memoize_multiple_calls(self):
            """Test that memoize caches result after first call."""
            class TestClass:
                def __init__(self):
                    self.counter = 0

                def a_method(self):
                    self.counter += 1
                    return self.counter

                @memoize
                def a_property(self):
                    return self.a_method()

            obj = TestClass()
            first = obj.a_property
            second = obj.a_property
            third = obj.a_property
            self.assertEqual(first, 1)
            self.assertEqual(second, 1)
            self.assertEqual(third, 1)
            self.assertEqual(obj.counter, 1)

        def test_memoize_different_instances(self):
            """Test that memoize does not share cache between instances."""
            class TestClass:
                def __init__(self, value):
                    self.value = value

                @memoize
                def a_property(self):
                    return self.value

            obj1 = TestClass(10)
            obj2 = TestClass(20)
            self.assertEqual(obj1.a_property, 10)
            self.assertEqual(obj2.a_property, 20)

        def test_memoize_with_args(self):
            """Test that memoize ignores method arguments (should only work for properties)."""
            class TestClass:
                @memoize
                def a_property(self):
                    return 99

            obj = TestClass()
            self.assertEqual(obj.a_property, 99)
            self.assertEqual(obj.a_property, 99)