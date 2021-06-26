set -e

python 001_metadata.py
python 101_create_curation_001_008.py
python 111_create_curation_each.py
python 701_create_index.py