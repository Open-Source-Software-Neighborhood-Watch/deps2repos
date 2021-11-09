"""Bioconda-related functionality"""

import os

from bioconda_utils.recipe import Recipe
from utils import find_all_paths, nested_dictionary_extract


def generate_bioconda_source_links(filepath):
    """Create list of of all bioconda-related links in directory.

    Can be used to create a list of all bioconda package source links
    in the bioconda registry.

    Args:
       filepath (str): filepath to a dir with 1 or more package.tomls

    Returns:
        list - all source links from all discovered meta.yaml files
    """
    all_links = []
    paths = find_all_paths(path_endings=["meta.yaml", "meta.yml"], base=filepath)
    for path in paths:
        links = parse_meta_dot_yaml_for_source_link(path)
        for link in links:
            all_links.append(link)

    return all_links


def parse_meta_dot_yaml_for_source_link(filepath):
    """Find source code link in meta.yaml file.

    Parsing meta.yaml conda files is not easy if done thoroughly
    because meta.yaml files are not YAML compliant given their
    use of jinja2 templating. The approach below is a simple hack
    given that the "home" yaml value indicates the source code
    management link for the project.

    Args:
       filepath (str) - path to the meta.yaml file to be parsed

    Returns:
        str - the source code link (e.g. GitHub) for the package

    """
    # Strip fname and keep path
    path = os.path.dirname(filepath)
    # This unusual call is a quirk of bioconda_utils.recipe
    recipe = Recipe.from_file(path, path)
    # Get link[s]
    links = list(nested_dictionary_extract("url", recipe.meta))

    return links
