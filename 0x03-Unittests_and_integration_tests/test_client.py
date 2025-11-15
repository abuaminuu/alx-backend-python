#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload."""
        mock_payload = {"org": org_name, "status": "active"}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, mock_payload)


    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL."""
        client = GithubOrgClient("test_org")
        expected_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
    
        # Mock the org property to return a known payload
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = expected_payload
            result = client._public_repos_url
            self.assertEqual(result, expected_payload["repos_url"])
