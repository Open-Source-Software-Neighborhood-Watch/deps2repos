"""PyPI-related functionality"""

import ast
import subprocess
import sys
import urllib
from urllib.parse import urlparse


import requests
import requirements


def parse_requirements_dot_text(filepath):
    """Convert requirements.txt to list of package names

    Args:
        filepath (str): filepath to a requirements.txt file

    Returns:
        pkgs: list of packages
    """

    # pylint: disable="no-member"

    pkgs = []
    with open(filepath, "r") as file:
        for req in requirements.parse(file):
            pkgs.append(req.name)

    return pkgs


def get_pypi_package_dependencies(pkg):
    """Determine dependencies for a PyPI package

    Use module pipgrip to create a dictionary of dependencies
    for a given Python package from PyPI.

    Args:
        pkg (str): the name of a python package found on PyPI

    Returns:
        dict_result: dict of package dependencies
    """
    command = f"pipgrip --json {pkg}"
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, check=True)

    # convert ouput to string and then dict
    str_result = result.stdout.decode("UTF-8")
    dict_result = ast.literal_eval(str_result)

    return dict_result


def get_pypi_data_json(pkg):
    """Return PyPI json associated with a python package.

    Args:
        pkg (str): the name of a python package found on PyPI

    Returns:
        dict: data related to a PyPI package
    """
    try:
        pkg_url = "https://pypi.org/pypi/" + pkg + "/json"
        response = requests.get(pkg_url)
        pypi_pkg_json = response.json()
    except urllib.error.HTTPError:
        print("ERROR: No such package on PyPI")
        sys.exit(1)  # 1 indicates error

    return pypi_pkg_json


def get_github_url_from_pypi_json(pypi_pkg_json):
    """Retrieve GitHub URL associated with a PyPI json.

    Search for potential GitHub URLs, identify them,
    and then return a properly formatted GitHub repository link.

    Args:
        pypi_pkg_json: a json blob of PyPI package data

    Returns:
        str: GitHub URL
    """
    github_page = ""
    potential_github_fields = []

    # check home page url
    if "github.com" in pypi_pkg_json["info"]["home_page"]:
        potential_github_fields.append(pypi_pkg_json["info"]["home_page"])

    # check project url fields if url fields present
    if pypi_pkg_json["info"]["project_urls"]:
        for _, url in pypi_pkg_json["info"]["project_urls"].items():
            if "github.com" in url:
                potential_github_fields.append(url)

    # check PyPI description text for any GitHub mentions
    description = pypi_pkg_json["info"]["description"]
    if potential_github_fields == [] and description:
        for token in description.split():
            if "github.com" in token:
                potential_github_fields.append(token)

    for field in potential_github_fields:
        # Any field with github in it must be github link
        if "github" in field:
            github_page = field
            break

    if github_page:
        page = urlparse(github_page)
        github_page = (
            # Only extract first couple parts of github page path to avoid
            # issues page, for instance
            "https://"
            + page.netloc
            + "/"
            + "/".join(page.path.split("/")[1:3])
        )

    return github_page
