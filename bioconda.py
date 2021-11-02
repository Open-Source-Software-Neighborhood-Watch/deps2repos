"""Bioconda-related functionality"""

from utils import clean_github_link, find_all_paths


def generate_bioconda_source_links(filepath):
    """Create list of of all bioconda-related links in directory.

    Can be used to create a list of all bioconda package source links
    in the bioconda registry.

    Args:
       filepath (str): filepath to a dir with 1 or more package.tomls

    Returns:
        list - all source links from all discovered meta.yaml files
    """
    links = []
    paths = find_all_paths(path_endings=["meta.yaml", "meta.yml"], base=filepath)
    for path in paths:
        link = parse_meta_dot_yaml_for_source_link(path)
        links.append(link)

    return links


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
    link = ""
    with open(filepath, "r") as meta_file:
        for line in meta_file.readlines():
            if "home" in line:
                link = clean_github_link(line)

    return link
