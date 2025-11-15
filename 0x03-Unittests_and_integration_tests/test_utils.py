#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

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

    @parameterized.expand(
        [
            ({}, ("a")),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exceptions(self, nested_map, path):
        """
        Test that KeyError is raised for invalid paths.
        Test that `access_nested_map` raises a KeyError for invalid paths.
        Args:
            nested_map (dict): The dictionary to access.
            path (tuple): The sequence of keys expected to cause KeyError.

        This test verifies that a KeyError is raised when attempting
        to access a key that does not exist in the nested dictionary.

        """
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        # assert the error message matches the missing key
        self.assertEqual(str(error.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """
    Tests for the get_json function in utils.py.
    Test case for the `get_json` utility function.
    Ensures that `get_json` correctly interacts with the `requests.get`
    method and returns the expected JSON data.
    """

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get) -> None:
        """
        Test that get_json returns expected result with mocked requests.get.
        Test that `get_json` returns the expected result when
        `requests.get` is mocked.

        Args:
            test_url (str): The URL to be passed into the `get_json` function.
            test_payload (Dict): The fake JSON payload returned by
            the mocked response.
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

        with patch.object(TestClass, "a_method", return_value=42) as mocked_method:
            # Call the memoized property twice
            first_call = obj.a_property
            second_call = obj.a_property

            # Ensure the property returns the correct result
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)

            # Assert that a_method was only called once
            mocked_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
