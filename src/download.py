#!/usr/bin/env python

import os
import requests
import sys
from io import BytesIO
from zipfile import ZipFile

NAER_ARCHIVE_URL = 'http://terms.naer.edu.tw/download/{category}/Term_{category}.zip/'

def load_all_categories() -> list[str]:
    """
    Helper function to load all category IDs from the repository when executed
    as a standalone script without specifying the desired category ID.
    """
    categories = []
    try:
        with open(os.path.join('data', 'categories.csv')) as f:
            for line in f:
                i = line.index(',')
                categories.append(line[:i])
            return categories
    except FileNotFoundError:
        print('Specify a category ID or run `load_categories.py` first.', file=sys.stderr)
        raise


def download_category(category: str) -> list[str]:
    """
    Download and extract the HTML data tables of a specific term category.
    Returns a list of paths of the extracted files.
    """

    # Download the ZIP archive from NAER website
    archive_url = NAER_ARCHIVE_URL.format(category=category)

    with requests.get(archive_url) as r:
        # Load the ZIP file and check its header
        zip_archive = ZipFile(BytesIO(r.content))
        assert zip_archive.testzip() is None

    # Recursively download and extract the HTML
    file_paths = []

    for zip_item in zip_archive.infolist():
        # Fix the file extension
        filename = zip_item.filename
        ext_index = filename.index('.xls')   # It’s actually HTML. LIES!

        # Change the extension and write them all into target directory
        file_path = os.path.join('data', 'html', filename[:ext_index] + '.html')
        with open(file_path, 'wb') as f:
            f.write(zip_archive.read(zip_item))

        file_paths.append(file_paths)
        print(f'Extracting {file_path}')

    return file_paths


def print_usage():
    print('Usage: download_terms.py [categories...]')


if __name__ == '__main__':
    if '--help' in sys.argv:
        print_usage()
    else:
        categories = sys.argv[1:] if len(sys.argv) > 1 else load_all_categories()
        for category in categories:
            download_category(category)
