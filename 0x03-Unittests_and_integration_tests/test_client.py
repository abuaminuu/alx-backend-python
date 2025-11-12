#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called exactly once with the right URL.
        """

        # Create a mock response
        mock_payload = {"org": org_name, "status": "active"}
        mock_get_json.return_value = mock_payload

        # Initialize the client with the test organization name
        client = GithubOrgClient(org_name)

        # Call the org property to trigger the HTTP fetch (mocked)
        result = client.org

        # Ensure get_json was called once with the correct API endpoint
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Check that the result matches the mock payload
        self.assertEqual(result, mock_payload)
