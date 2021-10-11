"""npm-related functionality."""

import json
import urllib

import requests


def js_package_dot_json_analysis(filepath):
    """Execute overall analysis of javascript's package.json

    Combines JavaScript-related functionality to perform end-to-end
    analysis of package.json. Prints output to terminal.

    # TODO: Keep track of packages that are either not on
    # npm or do not have a GitHub. Report to user.

    Args:
        filepath (str): filepath to a package.json file

    Returns:
        None
    """
    # retrieve only top-level packages
    top_level_pkgs = parse_package_dot_json(filepath)

    # create list of ALL dependencies, both top-level and transitive
    all_pkgs = []
    for pkg in top_level_pkgs:
        all_deps = get_npm_package_dependencies(pkg)
        for dep in all_deps:
            if dep not in all_pkgs:
                all_pkgs.append(dep)

    github_urls = []
    for pkg in all_pkgs:
        github_url = get_github_link_from_npm_api(pkg)
        github_urls.append(github_url)

    for url in github_urls:
        print(url)


def get_npm_package_dependencies(pkg):
    """Retrieve a list of package dependencies.

    Args:
        pkg (str) - package name

    Returns:
        dep_list - list of dependencies
    """
    # retrieve all package versions first
    try:
        pkg_url = "https://registry.npmjs.org/" + pkg
        response = requests.get(pkg_url)
        npm_pkg_json = response.json()
        pkg_versions = npm_pkg_json["versions"]
        # because python dicts are ordered as of 3.7, the last
        # item SHOULD be the most recent version. If this assumption
        # is wrong, this code is wrong
        last_version = list(pkg_versions)[-1]
    # TODO: handle error correctly and more gracefully
    except urllib.error.HTTPError as error:
        raise f"npm API error. Error: {error}"

    # find dependencies for most recent version
    dep_array = pkg_versions[last_version]["dependencies"]

    dep_list = []
    for dep in dep_array:
        dep_list.append(dep)

    return dep_list


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

    TODO: Keep only organization and package name from
    GitHub URL.

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
