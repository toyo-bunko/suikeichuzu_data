set -e

python 701_create_index.py
python 301_update_index.py
python 500_book.py