#!/usr/bin/env python

import re
import requests
import sys
from io import BytesIO
from zipfile import ZipFile

def load_all_categories():
    categories = []
    try:
        with open('raw_data/categories.csv') as f:
            for line in f:
                i = line.index(',')
                categories.append(line[:i])
            return categories
    except FileNotFoundError:
        print('Specify a category ID or run `get_term_categories.py` first.', file=sys.stderr)

def download_category(category):
    with requests.get(f'http://terms.naer.edu.tw/download/{category}/Term_{category}.zip/') as r:
        # Load the ZIP file and check its header
        zip_archive = ZipFile(BytesIO(r.content))
        assert zip_archive.testzip() is None

        # Recursively download and extract the HTML
        for zip_item in zip_archive.infolist():
            assert zip_item.filename.endswith('.xls')   # It’s actually HTML. LIES!
            zip_archive.extract(zip_item, path=f'raw_data/')

def print_usage():
    print('Usage: download_terms.py [categories...]')

if __name__ == '__main__':
    categories = sys.argv[1:] if len(sys.argv) > 1 else load_all_categories()
    for category in categories:
        download_category(category)
