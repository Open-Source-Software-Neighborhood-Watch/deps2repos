<img width="300" alt="deps2repos" src="https://user-images.githubusercontent.com/45634754/139943563-60f82e0c-890d-4650-bef1-b1957b5e7d11.png">

Convert dependency file into list of Git repositories

## Explanation
Have you ever wanted a list of all the GitHub links to the dependencies
of a Python (PyPI), JavaScript (npm), or Julia package? Then this is the repo
for you!

The Python/PyPI functionality is in beta stage. When a user selects Python,
this program returns the GitHub links for all top-level and transitive
dependencies.

The JavaScript/npm functionality is in less-than-beta-stage. When a user
selects Javascript, this program currently only returns the GitHub links
of the top-level dependencies and the dependencies of those top-level dependencies.
In other words, this tool does not **yet** traverse the entire npm dependency
list.

The Julia functionality is also in an early stage. When a user selects Julia, this
program identifies all package.toml files recursively in a directory and then outputs
each source code link associated with those packages.


## Installation

To install Bioconda functionality if you need to do Bioconda-related tasks, please follow instructions in [BIOCONDA-README.md](BIOCONDA-README.md)

To download:
```
git clone https://github.com/Open-Source-Software-Neighborhood-Watch
/deps2repos
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

For a Bioconda recipe[s] directory:

```
python main.py --bioconda [dirname]
```

For a Javascript package.json file:

```
python main.py --javascript [filename]
```

For analyzing the Julia registry or any folder containing Julia's package.toml's:
```
python main.py --julia [directory_name]
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
