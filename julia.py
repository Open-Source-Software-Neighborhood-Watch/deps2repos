"""Julia-related functionality"""

import os

import tomli


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


def find_package_dot_toml_path(pkg, base="."):
    """Find the path for a given julia package to its package.toml

    Args:
        pkg (str) - name of the julia package
        base (str) - location from which to start tree search

    Returns:
        str - the relative path to the correct package.toml
    """
    # find all directory paths
    dirs = [x[0] for x in os.walk(base)]
    # identify directory with the specified package name in it
    correct_dir = next(x for x in dirs if pkg in x)
    correct_path = correct_dir + "/package.toml"
    return correct_path
