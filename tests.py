"""Tests for deps2repos."""

import unittest

from pypi import get_pypi_data_json, get_github_url_from_pypi_json


class TestPypiMethods(unittest.TestCase):
    """Test PyPI-related methods."""

    def test_get_pypi_data_json(self):
        """Check PyPI API returns JSON."""
        self.requests_test_json = get_pypi_data_json("requests")
        self.assertTrue(self.requests_test_json)
        self.networkml_test_json = get_pypi_data_json("networkml")
        self.assertTrue(self.networkml_test_json)

    def test_get_github_url_from_pypi_json(self):
        """Check that GitHub link is returned from PyPI API json."""
        self.requests_test_json = get_pypi_data_json("requests")
        self.assertEqual(
            get_github_url_from_pypi_json(self.requests_test_json),
            "https://github.com/psf/requests",
        )
        self.requests_test_json = get_pypi_data_json("networkml")
        self.assertEqual(
            get_github_url_from_pypi_json(self.requests_test_json),
            "https://github.com/IQTLabs/NetworkML",
        )


if __name__ == "__main__":
    unittest.main()
