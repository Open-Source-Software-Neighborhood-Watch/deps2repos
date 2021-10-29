"""Implement CLI for deps2repos"""

import argparse

from npm import js_package_dot_json_analysis, js_txt_file_analysis
from pypi import python_requirements_dot_text_analysis


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
    parser.add_argument(
        "--javascript",
        default=False,  # default value is False
        help="Convert npm packages into GitHub links.",
    )
    parser.add_argument(
        "--no_deps",
        dest="no_deps",
        action="store_true",
        help="Whether to also analyze transitive dependencies.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_arguments()

    # parse specified Python requirements.txt file and generate GitHub links
    if args.python:
        python_requirements_dot_text_analysis(args.python, args.no_deps)

    # parse specified package.json and generate GitHub links
    # TODO: Analyze transitive dependencies too.
    if args.javascript:
        filepath = args.javascript
        if filepath.lower().endswith(".json"):
            js_package_dot_json_analysis(args.javascript)
        elif filepath.lower().endswith(".txt"):
            links = js_txt_file_analysis(args.javascript)
            for link in links:
                print(link)
