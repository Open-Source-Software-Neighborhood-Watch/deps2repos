
# Create bioconda-utils conda environment
git clone https://github.com/bioconda/bioconda-utils
cd bioconda-utils
conda create -y \
      --name deps2repos python=$1
conda install -y \
      --file bioconda_utils/bioconda_utils-requirements.txt \
      -c conda-forge -c bioconda
python setup.py install
cd ..
rm -rf bioconda-utils

# Install requirements in the conda environment
python -m pip install --upgrade pip
python -m pip install flake8 pytest
if [ -f requirements.txt ]; then
    python -m pip install -r requirements.txt;
fi
