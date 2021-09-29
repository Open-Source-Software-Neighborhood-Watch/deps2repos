"""Implement CLI for deps2repos"""

import argparse

from pypi import (
    get_github_url_from_pypi_json,
    get_pypi_data_json,
    get_pypi_package_dependencies,
    parse_requirements_dot_text,
)


def parse_command_line_arguments():
    """Parse command line arguments with argparse."""
    parser = argparse.ArgumentParser(
        description="Convert dependency files into list of GitHub links.",
        epilog="For help with this program, contact John Speed at jmeyers@iqt.org.",
    )
    parser.add_argument(
        "--python",
        default=False,  # default value is False
        help="Convert requirements.txt file into GitHub links.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_arguments()

    # parse specified Python requirements.txt file and generate GitHub links
    # for all top-level AND transitive dependencies.
    if args.python:

        top_level_pkgs = parse_requirements_dot_text(args.python)

        # Retrieve all dependencies, both top-level and transitive, and keep a
        # unique list
        all_pkgs = []
        for pkg in top_level_pkgs:
            all_deps = get_pypi_package_dependencies(pkg)
            for dep in all_deps:
                if dep not in all_pkgs:
                    all_pkgs.append(dep)

        # retrieve github urls for unique pypi packages
        github_urls = []
        for pkg in all_pkgs:
            pypi_json = get_pypi_data_json(pkg)
            github_url = get_github_url_from_pypi_json(pypi_json)
            if github_url:
                github_urls.append(github_url)

        for url in github_urls:
            print(url)
