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

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        # Assert the error message matches the missing key
        self.assertEqual(str(error.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """
    Tests for the get_json function in utils.py.
    Test case for the `get_json` utility function.
    Ensures that `get_json` correctly interacts with the `requests.get`
    method and returns the expected JSON data.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str, test_payload: dict, mock_get: Mock) -> None:
        """
        Test that get_json returns expected result with mocked requests.get.
        Test that `get_json` returns the expected result when
        `requests.get` is mocked.

        Args:
            test_url (str): The URL to be passed into the `get_json` function.
            test_payload (Dict): The fake JSON payload returned by the mocked response.
            mock_get (Mock): The patched version of `requests.get`.

        This test verifies that:
            - `requests.get` is called exactly once with the provided URL.
            - The JSON payload returned by `get_json` matches the mocked data.
        """
        # create mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # call the function
        result = get_json(test_url)

        # assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

if __name__ == "__main__":
    unittest.main()
