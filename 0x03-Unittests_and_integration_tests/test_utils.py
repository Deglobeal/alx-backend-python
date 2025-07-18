import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map"""

    @parameterized.expand([
        ("key_missing_in_empty_map", {}, ("a",), "a"),
        ("key_missing_in_nested_path", {"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path, expected_key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Debugging line (you can uncomment if needed)
        # print("Exception Message:", str(context.exception))
        self.assertEqual(str(context.exception), f"'{expected_key}'")
