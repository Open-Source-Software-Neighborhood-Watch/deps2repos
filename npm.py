"""npm-related functionality."""

import json
import urllib

import requests


def parse_package_dot_json(filepath):
    """Convert package.json to list of package names

    Args:
        filepath (str): filepath to a package.json file

    Returns:
        dep_list -  list of packages
    """
    with open(filepath) as json_file:
        data = json.load(json_file)

    deps = data["dependencies"]

    dep_list = []
    for dep in deps:
        dep_list.append(dep)

    return dep_list


def get_github_link_from_npm_api(pkg):
    """Retrieve github link for package from npm API

    TODO: Consider trimming off "git+" from beginning
    of URLs.

    Args:
        pkg (str) - package name

    Returns:
        github_link - URL to github
    """
    try:
        pkg_url = "https://registry.npmjs.org/" + pkg
        response = requests.get(pkg_url)
        npm_pkg_json = response.json()
        github_url = npm_pkg_json["repository"]["url"]
    # if no package found, return empty json
    except urllib.error.HTTPError as error:
        github_url = f"No GitHub found. Error: {error}"

    return github_url
