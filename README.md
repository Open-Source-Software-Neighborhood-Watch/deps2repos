# deps2repos
Convert dependency file into list of Git repositories



## Usage

For help:

```
python main.py --help
```

For a Python requirements.txt file:

```
python main.py --python [filename]
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

## Run Tests

```
python tests.py
```
