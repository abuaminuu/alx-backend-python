#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class."""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct 
        GithubOrgClient.org returns the payload."""
        mock_payload = {"org": org_name, "status": "active"}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, mock_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL."""
        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")

        def test_public_repos(self):
            pass