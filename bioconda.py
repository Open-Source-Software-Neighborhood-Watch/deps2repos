"""Bioconda-related functionality"""

import os

from bioconda_utils.recipe import Recipe
from utils import find_all_paths, clean_github_link, nested_dictionary_extract


def generate_bioconda_source_links(dirpath):
    """Create list of of all bioconda-related links in directory.

    Can be used to create a list of all bioconda package source links
    in the bioconda registry.

    Args:
       dirpath (str): dirpath to a bioconda recipe directory with 1 or more meta.yaml files

    Returns:
        list - all source links from all discovered meta.yaml files
    """
    # Using set() to ensure no duplicates
    all_links = set()
    paths = find_all_paths(path_endings=["meta.yaml", "meta.yml"], base=dirpath)
    for path in paths:
        links = parse_meta_dot_yaml_for_source_link(path)
        for link in links:
            all_links.add(link)

    return list(all_links)


def parse_meta_dot_yaml_for_source_link(filepath):
    """Find source code link in meta.yaml file.

    Parsing meta.yaml conda files is not easy if done thoroughly
    because meta.yaml files are not YAML compliant given their
    use of jinja2 templating. The approach below uses bioconda_utils
    to create the Recipe object from the meta.yaml file.

    Args:
       filepath (str) - path to the meta.yaml file to be parsed

    Returns:
        list - the source code link[s] (e.g. GitHub) for the package

    """
    links = []
    # Strip fname and keep path
    path = os.path.dirname(filepath)
    # This unusual call is a quirk of bioconda_utils.recipe
    recipe = Recipe.from_file(path, path)
    # Get link[s]
    raw_links = list(nested_dictionary_extract("url", recipe.meta))
    for raw_link in raw_links:
        link = clean_github_link(raw_link)
        if link:
            links.append(link)

    return links
