#!/usr/bin/env python

import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

NAER_BASE_URL = 'https://terms.naer.edu.tw'
NAER_INDEX_URL = 'https://terms.naer.edu.tw/download/1/?page_size=1000'

date_format_expr = re.compile(r'(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日\s+(?P<hour>0?\d|\d{2}):(?P<minute>\d{2})')

def parse_date(string: str) -> datetime:
    if m := date_format_expr.fullmatch(string):
        year, month, day, hour, minute = int(m['year']), int(m['month']), int(m['day']), int(m['hour']), int(m['minute'])
        return datetime(year, month, day, hour, minute)
    raise ValueError('Failed to parse string as date')


def load_categories(file=None) -> list[tuple[str, str, datetime, str]]:
    """
    Downloads all the categories listed on the Download page of NAER.
    Returns a list of tuples (ID, name, last updated on, data file URL).
    """

    # Defaults to stdout
    file = file or sys.stdout

    with requests.get(NAER_INDEX_URL) as r:
        soup = BeautifulSoup(r.text, 'html.parser')

    categories = []
    for row in soup.css.select('#pageContent div.table-rwd > div.tbody > div.tr'):
        cat_id = int(row.select_one('input[name="num"]')['value'])
        name = row.select_one('div.td[aria-label="領域類別"]').string.strip()
        last_updated = parse_date(row.select_one('div.td[aria-label="更新日期"]').string.strip())
        data_url = urljoin(NAER_BASE_URL, row.select_one('a[title="下載"]')['href'])

        categories.append((cat_id, name, last_updated, data_url))
        print(cat_id, name, last_updated.isoformat(sep=' '), data_url, sep=',', file=file)

    return categories


def print_usage():
    print('Usage: src/load_categories.py [-]')


if __name__ == '__main__':
    if '-' in sys.argv:
        load_categories()   # Write to stdout
    elif '--help' in sys.argv:
        print_usage()
    else:
        with open(os.path.join('data', 'categories.csv'), 'w+') as f:
            load_categories(file=f)
