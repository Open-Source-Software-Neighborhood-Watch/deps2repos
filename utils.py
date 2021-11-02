"""Utility functions across ecosystems."""

import glob
import re


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
        cleaned_url = cleaned_url.strip("\n")
    except AttributeError:
        cleaned_url = ""
    return cleaned_url


def find_all_paths(path_endings, base="."):
    """Find all paths with particular ending.

    Args:
        base (str) - location from which to start tree search
        path_ending (list of str) - a path ending such as package.toml

    Returns:
        list - all relative paths ending in path_ending
    """
    paths = []
    for path_ending in path_endings:
        found_paths = glob.glob(base + "/**/" + path_ending, recursive=True)
        paths.extend(found_paths)
    return paths
