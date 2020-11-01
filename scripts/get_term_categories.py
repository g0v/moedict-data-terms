#!/usr/bin/env python

import os
import re
import requests
import sys

NAER_INDEX_URL = 'http://terms.naer.edu.tw/download/'

def load_categories(file=None) -> list[tuple[str, str, str]]:
    """
    Downloads all the categories listed on the Download page of NAER.
    Returns a list of tuples (ID, name, last updated on).
    """

    # Defaults to stdout
    file = file or sys.stdout

    with requests.get(NAER_INDEX_URL) as r:
        response = r.text

    pattern = re.compile(r'<a href="/download/(?P<id>\d+)/" title="最後修改 (?P<last_updated>[\d \-\:]+)">(?P<name>[^<]+)</a>')
    categories = []
    for match in pattern.finditer(response):
        cat_id, name, last_updated = match['id'], match['name'], match['last_updated']
        categories.append((cat_id, name, last_updated))
        print(cat_id, name, last_updated, sep=',', file=file)

    return categories


def show_empty_categories(file=None) -> list[str]:
    """
    Downloads and list all categories without available exports on NAER.
    Returns a list of category names, as no IDs are provided.
    """

    # Defaults to stderr
    file = file or sys.stderr

    with requests.get(NAER_INDEX_URL) as r:
        response = r.text

    # Bonus: warns about categories without files
    empty_pattern = re.compile(r'<a href="" title="沒有檔案" onclick="return false;">(?P<name>[^<]+)</a>')
    categorie_names = []
    for match in empty_pattern.finditer(response):
        categorie_names.append(match['name'])
        print('WARN: No file provided by', match['name'], file=file)

    return categorie_names


def print_usage():
    print('Usage: get_term_categories.py [-]')


if __name__ == '__main__':
    if '-' in sys.argv:
        load_categories()   # Write to stdout
    elif '--help' in sys.argv:
        print_usage()
    else:
        with open(os.path.join('raw_data', 'categories.csv'), 'r') as f:
            load_categories(file=f)

    # NOTE: Categories without available file to download are only the names of
    # non-Anglosphere Nobel prize winners for now; so we are not printing them
    # at this point.
