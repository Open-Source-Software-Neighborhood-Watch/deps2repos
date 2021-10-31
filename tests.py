"""Tests for deps2repos."""

import unittest

from julia import (
    extract_repo_link_from_toml_dict,
    find_all_package_dot_toml_paths,
    find_package_dot_toml_path,
    parse_julia_package_dot_toml,
)
from pypi import (
    get_github_url_from_pypi_json,
    get_pypi_data_json,
    get_pypi_package_dependencies,
    parse_requirements_dot_text,
)
from npm import (
    clean_github_link,
    get_github_link_from_npm_api,
    js_txt_file_analysis,
    parse_package_dot_json,
    get_npm_package_dependencies,
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


class TestNpmMethods(unittest.TestCase):
    """Test npm-related methods."""

    def test_parse_package_dot_json(self):
        """Check parsing package.json files"""
        self.test_package_json = parse_package_dot_json("test/test_package.json")
        self.assertEqual(len(self.test_package_json), 5)
        self.assertEqual(
            self.test_package_json,
            [
                "@fortawesome/fontawesome",
                "@fortawesome/fontawesome-svg-core",
                "@fortawesome/free-solid-svg-icons",
                "@fortawesome/react-fontawesome",
                "d3",
            ],
        )

    def test_js_txt_file_analysis(self):
        """Check parsing .txt file of npm packages and returning src links"""
        self.test_source_link_list = js_txt_file_analysis("test/test_npm_packages.txt")
        self.assertEqual(len(self.test_source_link_list), 2)
        self.assertEqual(
            self.test_source_link_list,
            [
                "https://github.com/lodash/lodash.git",
                "https://github.com/facebook/react.git",
            ],
        )

    def test_get_github_url_from_npm_api(self):
        """Check that GitHub link is returned from npm API json."""
        self.d3_github_link_test = get_github_link_from_npm_api("d3")
        self.assertEqual(
            self.d3_github_link_test,
            "https://github.com/d3/d3.git",
        )
        self.doesnt_exist_github_link_test = get_github_link_from_npm_api("d3xjhdfh")
        self.assertEqual(
            self.doesnt_exist_github_link_test,
            [],
        )

    def test_get_npm_package_dependencies(self):
        """Test get_npm_package_dependencies function."""
        self.d3_dep_list_test = get_npm_package_dependencies("d3-zoom")
        self.assertEqual(
            self.d3_dep_list_test,
            [
                "d3-dispatch",
                "d3-drag",
                "d3-interpolate",
                "d3-selection",
                "d3-transition",
            ],
        )
        self.doesnt_exist_dep_list_test = get_npm_package_dependencies("d3-zoom-xxxxx")
        self.assertEqual(
            self.doesnt_exist_dep_list_test,
            [],
        )

    def test_clean_github_link(self):
        """Test clean_github_link function."""
        self.assertEqual(
            clean_github_link(
                "git+https://www.github.com/psf/requests/tree/main/requests"
            ),
            "https://www.github.com/psf/requests",
        )
        self.assertEqual(
            clean_github_link("https://github.com/psf/requests/tree/main/requests"),
            "https://github.com/psf/requests",
        )


class TestJuliaMethods(unittest.TestCase):
    """Test Julia-related methods."""

    def test_parse_julia_package_dot_toml(self):
        """Check parsing package.toml files"""
        self.test_package_toml_dict = parse_julia_package_dot_toml(
            "test/test_julia_package.toml"
        )
        self.assertEqual(
            self.test_package_toml_dict,
            {
                "name": "AAindex",
                "uuid": "1cd36ffe-cb05-4761-9ff9-f7bc1999e190",
                "repo": "https://github.com/jowch/AAindex.jl.git",
            },
        )

    def test_extract_repo_link_from_toml_dict(self):
        """Check extracting repo link from toml dict"""
        self.test_package_toml_dict = parse_julia_package_dot_toml(
            "test/test_julia_package.toml"
        )
        self.test_repo_link = extract_repo_link_from_toml_dict(
            self.test_package_toml_dict
        )
        self.assertEqual(self.test_repo_link, "https://github.com/jowch/AAindex.jl.git")

    def test_find_all_package_dot_toml_paths(self):
        """Check find_all_package_dot_toml_paths()."""
        self.test_toml_paths = find_all_package_dot_toml_paths("test")
        self.assertEqual(
            self.test_toml_paths,
            [
                "test/julia_package_tree/ADI/package.toml",
                "test/julia_package_tree/ACME/package.toml",
            ],
        )

    def test_find_package_dot_toml_path(self):
        """Check finding correct package.toml"""
        self.test_toml_paths = find_all_package_dot_toml_paths("test")
        self.test_package_dot_toml_path = find_package_dot_toml_path(
            pkg="ACME", toml_path_list=self.test_toml_paths
        )
        self.assertEqual(
            self.test_package_dot_toml_path, "test/julia_package_tree/ACME/package.toml"
        )


if __name__ == "__main__":
    unittest.main()
