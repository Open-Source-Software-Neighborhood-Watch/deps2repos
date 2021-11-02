"""Julia-related functionality"""

import glob

import tomli

from utils import find_all_paths


def generate_julia_source_links(filepath):
    """Create list of of all julia-related links in directory.

    Can be used to create a list of all julia package links
    in the Julia registry.

    Args:
       filepath (str): filepath to a dir with 1 or more package.tomls

    Returns:
        list - all source links from all discovered package.toml files
    """
    links = []
    paths = find_all_paths(path_endings=["package.toml"], base=filepath)
    for path in paths:
        toml_dict = parse_julia_package_dot_toml(path)
        link = extract_repo_link_from_toml_dict(toml_dict)
        links.append(link)

    return links


def parse_julia_package_dot_toml(filepath):
    """Convert julia package toml into dict.

    Args:
       filepath (str): filepath to a toml file

    Returns:
        dict - the toml file values
    """
    with open(filepath, "rb") as toml_file:
        toml_dict = tomli.load(toml_file)

    return toml_dict


def extract_repo_link_from_toml_dict(toml_dict):
    """Extract the repo (e.g. GitHub) link from the toml dict.

    Args:
        toml_dict (dict) - the toml file values

    Returns:
        str - the repo link
    """
    return toml_dict["repo"]


def find_package_dot_toml_path(pkg, toml_path_list):
    """Find the path for a given julia package to its package.toml

    Args:
        pkg (str) - name of the julia package
        toml_path_list (str) - paths of all package.toml files to search

    Returns:
        str - the relative path to the correct package.toml
    """
    pkg_path = next(x for x in toml_path_list if pkg in x)
    return pkg_path
