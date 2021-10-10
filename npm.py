"""npm-related functionality."""

import json

def parse_package_dot_json(filepath):
    """Convert package.json to list of package names

    Args:
        filepath (str): filepath to a package.json file

    Returns:
        pkgs: list of packages
    """
    with open('test/test_package.json') as json_file:
        data = json.load(json_file)

    deps = data["dependencies"]

    dep_list = []
    for dep in deps:
        dep_list.append(dep)

    return dep_list
