"""Tests for deps2repos."""

import unittest

from pypi import (
    get_github_url_from_pypi_json,
    get_pypi_data_json,
    get_pypi_package_dependencies,
    parse_requirements_dot_text,
)

# pylint: disable="attribute-defined-outside-init"


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

    def test_get_pypi_package_dependencies(self):
        """Check that pipgrip produces dependency list."""
        self.requests_test_deps = get_pypi_package_dependencies("requests")
        self.assertEqual(len(self.requests_test_deps), 5)
        self.assertTrue(self.requests_test_deps["certifi"])

    def test_parse_requirements_dot_text(self):
        """Check parsing requirements.txt files"""
        self.test_requirements = parse_requirements_dot_text(
            "test/test_requirements.txt"
        )
        self.assertEqual(len(self.test_requirements), 3)
        self.assertEqual(
            self.test_requirements, ["package_a", "package_b", "package_c"]
        )


if __name__ == "__main__":
    unittest.main()
