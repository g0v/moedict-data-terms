#!/usr/bin/env python

import csv
import os
import requests
import sys
from .models import Category, restore, save
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile

def load_all_categories() -> list[Category]:
    """
    Helper function to load all category IDs from the repository when executed
    as a standalone script without specifying the desired category ID.
    """
    try:
        with open(os.path.join('data', 'categories.csv'), newline='') as f:
            return restore(f)
    except FileNotFoundError:
        print('Specify a category ID or run `load_categories.py` first.', file=sys.stderr)
        raise


def download_category(data_url: str) -> list[str]:
    """
    Download and extract the HTML data tables of a specific term category.
    Returns a list of paths of the extracted files.
    """

    # Download the ZIP archive from NAER website
    with requests.get(data_url) as r:
        # Load the ZIP file and check its header
        zip_archive = ZipFile(BytesIO(r.content))
        assert zip_archive.testzip() is None

    # Recursively download and extract the HTML
    file_paths = []

    for zip_item in zip_archive.infolist():
        # Make sure files are in ODS format
        filename = zip_item.filename
        assert filename.endswith('.ods')

        # Write them all into target directory
        file_path = os.path.join('data', filename)
        with open(file_path, 'wb') as f:
            f.write(zip_archive.read(zip_item))

        file_paths.append(file_paths)
        print(f'Extracting {file_path}')

    return file_paths


def print_usage():
    print('Usage: src/download_terms.py [categories...]')


if __name__ == '__main__':
    if '--help' in sys.argv:
        print_usage()
    else:
        categories = sys.argv[1:] if len(sys.argv) > 1 else [c.data_url for c in load_all_categories()]
        for category in categories:
            download_category(category)
