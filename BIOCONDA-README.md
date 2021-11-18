This README is for installation of deps2repos including Bioconda recipe functionality. You do not need to follow installation instructions in [README.md](README.md) as well.

## Installation

To download:
```
git clone https://github.com/IQTLabs/deps2repos
```

Download Bioconda-utils and Bioconda-recipes

```
git clone https://github.com/bioconda/bioconda-utils
```
```
git clone https://github.com/bioconda/bioconda-recipes
```

Create Conda Environment
```
conda create --name deps2repos
```
Activate Conda
```
conda activate deps2repos
```
Install bioconda-utils
```
cd bioconda-utils
conda install --file bioconda_utils/bioconda_utils-requirements.txt -c conda-forge -c bioconda 
python setup.py install
cd ..
```

To download dependencies:
```
cd deps2repos
pip install -r requirements.txt
```
## Usage

For a Bioconda recipe[s] directory:

```
python main.py --bioconda [dirname]
```
