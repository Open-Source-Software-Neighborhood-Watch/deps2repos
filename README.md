# deps2repos
Convert dependency file into list of Git repositories


## Explanation
Have you ever wanted a list of all the GitHub links to the dependencies
of a Python (PyPI) or JavaScript (npm) package? Then this is the repo
for you!

The Python/PyPI functionality is in beta stage. When a user selects Python,
this program returns the GitHub links for all top-level and transitive
dependencies.

The JavaScript/npm functionlity is in less-than-beta-stage. When a user
selects Javascript, this program currently only returns the GitHub links
of the top-level dependencies and the dependencies of those top-level dependencies.
In other words, this tool does not **yet** traverse the entire npm dependency
list.


## Installation

To download:
```
git clone https://github.com/IQTLabs/deps2repos
```

To download dependencies:
```
pip install -r requirements.txt
```

## Usage

For help:

```
python main.py --help
```

For a Python requirements.txt file:

```
python main.py --python [filename]
```

For a Javascript package.json file:

```
python main.py --javascript [filename]
```

Example command using deps2repos's own requirements.txt as input.

```
python main.py --python requirements.txt
```

Example output:

```
WARNING: Some of the packages found on PyPI do not have GitHubs:
pkginfo

https://github.com/c0fec0de/anytree
https://github.com/benjaminp/six
https://github.com/certifi/python-certifi
https://github.com/ousret/charset_normalizer
https://github.com/pallets/click
https://github.com/python/importlib_metadata
https://github.com/python/typing
https://github.com/jaraco/zipp
https://github.com/kjd/idna
https://github.com/pypa/packaging
https://github.com/pyparsing/pyparsing
https://github.com/pypa/pip
https://github.com/ddelange/pipgrip
https://github.com/pypa/setuptools
https://github.com/pypa/wheel
https://github.com/psf/requests
https://github.com/urllib3/urllib3
https://github.com/davidfischer/requirements-parser
```

To analyze only the dependencies explicitly stated in the requirements.txt file, use the
`no-deps` flag (only works for PyPI currently):

```
python main.py --no_deps --python [filename]
```


## Run Tests

```
python tests.py
```
