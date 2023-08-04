#!/usr/bin/env python

import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

NAER_BASE_URL = 'https://terms.naer.edu.tw'
NAER_INDEX_URL = 'https://terms.naer.edu.tw/download/1/?page_size=1000'

def load_categories(file=None) -> list[tuple[str, str, str, str]]:
    """
    Downloads all the categories listed on the Download page of NAER.
    Returns a list of tuples (ID, name, last updated on).
    """

    # Defaults to stdout
    file = file or sys.stdout

    with requests.get(NAER_INDEX_URL) as r:
        soup = BeautifulSoup(r.text, 'html.parser')

    categories = []
    for row in soup.css.select('#pageContent div.table-rwd > div.tbody > div.tr'):
        cat_id = int(row.select_one('input[name="num"]')['value'])
        name = row.select_one('div.td[aria-label="領域類別"]').string.strip()
        last_updated = row.select_one('div.td[aria-label="更新日期"]').string.strip()
        data_url = urljoin(NAER_BASE_URL, row.select_one('a[title="下載"]')['href'])

        categories.append((cat_id, name, last_updated, data_url))
        print(cat_id, name, last_updated, data_url, sep=',', file=file)

    return categories


def print_usage():
    print('Usage: load_categories.py [-]')


if __name__ == '__main__':
    if '-' in sys.argv:
        load_categories()   # Write to stdout
    elif '--help' in sys.argv:
        print_usage()
    else:
        with open(os.path.join('data', 'categories.csv'), 'w+') as f:
            load_categories(file=f)
