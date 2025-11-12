#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, sum, get_json, memoize

"""
Unit tests for the `utils.get_json` function.

This module tests that the `get_json` function correctly retrieves
and returns JSON data from a given URL. The HTTP requests are mocked
to ensure no real network calls are made during testing.
"""


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function.
    Test case for the `utils.access_nested_map` function.
    Ensures that nested map access works as expected, both for valid paths
    and for paths that should raise exceptions.
    """

    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns correct value for
        given path. Test that `access_nested_map` returns the
        expected value for valid paths.
        Args:
            nested_map (dict): The dictionary to access.
            path (tuple): The sequence of keys to traverse.
            expected (any): The expected value returned by the
            function.

        This test verifies that the function correctly retrieves values
        from nested dictionaries without raising exceptions.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    
if __name__ == "__main__":
    unittest.main()
