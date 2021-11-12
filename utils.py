"""Utility functions across ecosystems."""

import glob
import os
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
        found_paths = glob.glob(
            os.path.expanduser(base) + "/**/" + path_ending, recursive=True,
        )
        paths.extend(found_paths)
    return paths


def nested_dictionary_extract(key, dictionary):
    """Find all values of specific key in nested dictionary/list

    Args:
        key (str) - key for which to search
        dictionary (dict) - dictionary through which to search. Can be
            nested with lists included

    Returns:
        generator - contains all values of search key
    """
    if isinstance(dictionary, list):
        for i in dictionary:
            for x in nested_dictionary_extract(key, i):
                yield x
    elif isinstance(dictionary, dict):
        if key in dictionary:
            yield dictionary[key]
        for j in dictionary.values():
            for x in nested_dictionary_extract(key, j):
                yield x
