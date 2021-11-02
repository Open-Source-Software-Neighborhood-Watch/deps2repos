"""Bioconda-related functionality"""

from utils import clean_github_link


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
    with open(filepath, "r") as f:
        for line in f.readlines():
            if "home" in line:
                link = clean_github_link(line)

    return link
