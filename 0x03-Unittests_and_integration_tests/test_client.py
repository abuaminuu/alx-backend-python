#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class.
Test that GithubOrgClient.org returns the correct
GithubOrgClient.org returns the payload.
Test that GithubOrgClient.org returns the correct Test
that GithubOrgClient.org returns the correct"""

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


        @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""

        # Payload returned by mocked get_json
        fake_payload = [
            {"name": "repo1", "private": False},
            {"name": "repo2", "private": False},
        ]
        mock_get_json.return_value = fake_payload

        # Mock _public_repos_url to return a fake URL
        client = GithubOrgClient("test_org")
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://fakeurl.com/repos"
            result = client.public_repos()

            # Ensure the result matches the repo names in the payload
            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)

            # Assert both mocks were called once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fakeurl.com/repos")
