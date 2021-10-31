"""Julia-related functionality"""

import glob

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


def find_all_package_dot_toml_paths(base="."):
    """Find all package.toml paths.

    Args:
        base (str) - location from which to start tree search

    Returns:
        list - the relative paths to all package.toml files

    """
    paths = glob.glob(base + "/**/package.toml", recursive=True)
    return paths


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


# TODO: function for downloading most recent julia repository
