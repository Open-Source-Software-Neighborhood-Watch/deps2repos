"""npm-related functionality."""

import csv
import json
import re

import requests


def js_package_dot_json_analysis(filepath):
    """Execute overall analysis of javascript's package.json

    Combines JavaScript-related functionality to perform end-to-end
    analysis of package.json. Prints output to terminal.

    Args:
        filepath (str): filepath to a package.json file

    Returns:
        None
    """
    # retrieve only top-level packages
    top_level_pkgs = parse_package_dot_json(filepath)

    # create list of ALL dependencies, both top-level and transitive
    # TODO: consider simplifying logic, too many branches
    all_pkgs = []
    pkgs_without_dependencies = []
    for pkg in top_level_pkgs:
        all_deps = get_npm_package_dependencies(pkg)
        if all_deps:
            for dep in all_deps:
                if dep not in all_pkgs:
                    all_pkgs.append(dep)
        # TODO: likely need to differentiate between packages with no
        # dependencies (which is rare, but does happen in npm) and package
        # not on npm
        # TODO: create category of packages that do not list dependencies,
        # not packages without dependencies
        else:
            pkgs_without_dependencies.append(pkg)

    github_urls = []
    pkgs_without_github_urls = []
    for pkg in all_pkgs:
        github_url = get_github_link_from_npm_api(pkg)
        if github_url:
            github_urls.append(github_url)
        else:
            pkgs_without_github_urls.append(pkg)

    # print all results, making sure to print any packages without
    # an npm entry or without dependencies (no dependencies is rare in npm)
    # and also packages without a GitHub link
    if pkgs_without_dependencies:
        print(
            "\nWARNING: Some of these packages are either not on npm or do not have dependencies."
        )
        for pkg in pkgs_without_dependencies:
            print(pkg)
        print("")

    if pkgs_without_github_urls:
        print("\nWARNING: Some of these packages do not have a GitHub URL.")
        for pkg in pkgs_without_github_urls:
            print(pkg)
        print("")

    for url in github_urls:
        print(url)


def js_txt_file_analysis(filepath):
    """Retrieve source code links for npm packages listed in .txt file

    Combines JavaScript-related functionality to return source code links
    (such as GitHub) for npm packages listed line by line in a .txt file

    Args:
        filepath (str): filepath to a .txt file

    Returns:
        (list) packages
    """
    # extract npm packages line-by-line into list
    pkgs = []
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            pkgs.append(row[0])

    links = []
    for pkg in pkgs:
        link = get_github_link_from_npm_api(pkg)
        links.append(link)

    return links


def get_npm_package_dependencies(pkg):
    """Retrieve a list of package dependencies.

    Args:
        pkg (str) - package name

    Returns:
        dep_list - list of dependencies
    """
    npm_pkg_json = requests.get("https://registry.npmjs.org/" + pkg).json()

    # check if npm contains package
    if npm_pkg_json == {"error": "Not found"}:
        dep_list = []
    else:
        # retrieve all package versions
        pkg_versions = npm_pkg_json["versions"]
        # because python dicts are ordered as of 3.7, the last
        # item SHOULD be the most recent version. If this assumption
        # is wrong, this code is wrong
        last_version = list(pkg_versions)[-1]

        # find dependencies for most recent version
        try:
            dep_array = pkg_versions[last_version]["dependencies"]
        # if these keys are not present, simply return empty list
        # to avoid crash
        except KeyError:
            dep_array = []

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


def clean_github_link(raw_url):
    """Convert raw URL into GitHub link with org and repo.

    Convert a raw URL into cleaned URL, where a cleaned url
    has https://www.github.com/{org}/{package}

    Args:
        raw_url (str) - raw URL from npm

    Returns
        cleaned_url: string
    """
    # make https:// optional
    # make www. optional
    # check for a organization name after github.com and a package name
    pattern = re.compile("(https://)?(www.)?github.com/[^/]*/[^/]*")
    try:
        cleaned_url = pattern.search(raw_url).group(0)
    except AttributeError:
        cleaned_url = ""
    return cleaned_url


def get_github_link_from_npm_api(pkg):
    """Retrieve github link for package from npm API

    Args:
        pkg (str) - package name

    Returns:
        clean_github_url - URL to github, empty if package not found
    """
    npm_pkg_json = requests.get("https://registry.npmjs.org/" + pkg).json()

    # check if npm contains package
    if npm_pkg_json == {"error": "Not found"}:
        clean_github_url = []
    else:
        try:
            github_url = npm_pkg_json["repository"]["url"]
            # only clean link if link exists
            if github_url:
                clean_github_url = clean_github_link(github_url)
            else:
                clean_github_url = []
        # if ["repository"]["url"] keys are not present, simply return
        # empty list to avoid crash
        except KeyError:
            clean_github_url = []

    return clean_github_url
