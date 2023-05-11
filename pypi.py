"""PyPI-related functionality"""

import ast
import subprocess
import urllib


import requests
import requirements

from utils import clean_github_link


def python_requirements_dot_text_analysis(filepath, no_deps):
    """Execute overall analysis of Python's requirements.txt

    Combines python-related functionality to perform end-to-end
    analysis of requirements.txt. Prints output to terminal.

    Selecting no_deps switch means no dependencies other than
    those explicitly specified are analyzed.

    Args:
        filepath (str): filepath to a requirements.txt file
        no_deps (bool): whether to analyze dependencies too

    Returns:
        None
    """
    # pylint: disable=too-many-branches
    top_level_pkgs = parse_requirements_dot_text(filepath)

    # Retrieve all dependencies, both top-level and transitive, and keep a
    # unique list
    all_pkgs = []
    # skip adding transitive dependencies if no_deps selected
    if no_deps:
        all_pkgs = top_level_pkgs
    else:
        for pkg in top_level_pkgs:
            all_deps = get_pypi_package_dependencies(pkg)
            for dep in all_deps:
                if dep not in all_pkgs:
                    all_pkgs.append(dep)

    # retrieve github urls for unique pypi packages and store date
    # on any packages without a PyPI entry or a gitHub
    github_urls = []
    pkgs_without_pypi_data = []
    pkgs_without_githubs = []
    for pkg in all_pkgs:

        pypi_json = get_pypi_data_json(pkg)
        if not pypi_json:
            pkgs_without_pypi_data.append(pkg)

        github_url = get_github_url_from_pypi_json(pypi_json)
        if pypi_json and not github_url:
            pkgs_without_githubs.append(pkg)

        if github_url:
            github_urls.append(github_url)

    # print all results, making sure to print any packages without
    # a PyPI entry or GitHub first to ensure an informed user
    if pkgs_without_pypi_data:
        print("\nWARNING: Some of these packages are not on PyPI:")
        for pkg in pkgs_without_pypi_data:
            print(pkg)
        print("")

    if pkgs_without_githubs:
        print("\nWARNING: Some of the packages found on PyPI do not have GitHubs:")
        for pkg in pkgs_without_githubs:
            print(pkg)
        print("")

    for url in github_urls:
        print(url)


def parse_requirements_dot_text(filepath):
    """Convert requirements.txt to list of package names

    TODO: considering making this parsing more general such that
    pipfiles can be parsed too. See this library for one
    potential solution: https://github.com/sarugaku/requirementslib

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
    try:
        command = f"pipgrip --json {pkg}"
        result = subprocess.run(command.split(), capture_output=True, check=True)

        # convert ouput to string and then dict
        str_result = result.stdout.decode("UTF-8")
        dict_result = ast.literal_eval(str_result)
    # if pkg doesn't exist, return empty dict
    except subprocess.CalledProcessError:
        dict_result = {}

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
    # if no package found, return empty json
    except urllib.error.HTTPError:
        pypi_pkg_json = {}

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
    if pypi_pkg_json["info"]["home_page"] is not None and "github.com" in pypi_pkg_json["info"]["home_page"]:
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
        github_page = clean_github_link(github_page)

    return github_page
