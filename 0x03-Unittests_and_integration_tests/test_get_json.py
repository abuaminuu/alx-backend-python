#!/usr/bin/env python3
"""
Tests for get_json.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


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



class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class."""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
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
        """Test that _public_repos_url returns the correct URL."""
        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
            result = client._public_repos_url
            self.(assertEqual(result, "https://api.github.com/orgs/test_org/repos"))
