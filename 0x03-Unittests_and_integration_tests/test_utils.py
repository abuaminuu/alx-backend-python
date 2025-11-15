#!/usr/bin/env python3
"""
Unit tests for utils.py (access_nested_map, get_json, memoize)
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, memoize, get_json
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct dictionary path access."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(str(error.exception), repr(path[-1]))


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator"""

    def test_memoize(self):
        """Test that a memoized method caches the result after first call"""

        class TestClass:
            """Sample class to test memoization"""

            def a_method(self) -> int:
                """Returns a fixed integer"""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized property that calls a_method"""
                return self.a_method()

        obj = TestClass()

        # me = mocked_method
        with patch.object(TestClass, "a_method", return_value=42) as me:
            # Call the memoized property twice
            first_call = obj.a_property
            second_call = obj.a_property

            # Ensure the property returns the correct result
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)

            # Assert that a_method was only called once
            me.assert_called_once()


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, url, payload, mock_get):
        """Test JSON retrieval with mocked requests.get."""
        mock_response = Mock()
        mock_response.json.return_value = payload
        mock_get.return_value = mock_response

        result = get_json(url)

        mock_get.assert_called_once_with(url)
        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main()
