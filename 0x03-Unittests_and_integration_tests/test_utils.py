#!/usr/bin/env python3
"""
Unit tests for utils.py: access_nested_map, get_json, memoize
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(str(error.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, url, payload, mock_get):
        """Test that get_json returns the expected payload."""
        mock_response = Mock()
        mock_response.json.return_value = payload
        mock_get.return_value = mock_response

        result = get_json(url)

        mock_get.assert_called_once_with(url)
        self.assertEqual(result, payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self):
        """Test that a memoized method caches the result after first call."""

        class TestClass:
            """Helper class to test memoization."""

            def a_method(self):
                """Method to be memoized."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        obj = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            first = obj.a_property
            second = obj.a_property

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
