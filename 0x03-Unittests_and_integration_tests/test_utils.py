#!/usr/bin/env python3
"""
Unit test module for the utils.access_nested_map function.
Ensures correct behavior for various nested dictionary path lookups.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Unit test class for verifying correct behavior of access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object) -> None:
        """Test that access_nested_map returns expected values for given inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
