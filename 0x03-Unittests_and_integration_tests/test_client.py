#!/usr/bin/env python3
 
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures  # Assuming fixtures.py is in the same directory or PYTHONPATH


class TestGithubOrgClient(unittest.TestCase):
    # 4. Parameterize and patch get_json called once with expected arg
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        result = client.org()
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

    # 5. Mocking a property (_public_repos_url)
    def test_public_repos_url(self):
        client = GithubOrgClient("test_org")
        payload = {"repos_url": "http://some.url/api/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    # 6. Patch get_json (decorator) and _public_repos_url (context manager) for public_repos
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fakeurl/api/repos"
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fakeurl/api/repos")

    # 7. Parameterize test_has_license
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


# 8. Integration test with fixtures and patching requests.get
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            fixtures.org_payload,
            fixtures.repos_payload,
            fixtures.expected_repos,
            fixtures.apache2_repos,
        )
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/google":
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url == "https://api.github.com/orgs/google/repos":
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            raise ValueError(f"Unmocked url {url}")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_apache2_license(self):
        client = GithubOrgClient("google")
        repos = client.public_repos(license_key="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
