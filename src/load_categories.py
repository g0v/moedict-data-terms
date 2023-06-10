#!/usr/bin/env python

import os
import re
import requests
import sys
from .models import Category, save
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


def download_categories() -> list[Category]:
    """
    Downloads all the categories listed on the Download page of NAER.
    Returns a list of tuples (ID, name, last updated on, data file URL).
    """

    with requests.get(NAER_INDEX_URL) as r:
        soup = BeautifulSoup(r.text, 'html.parser')

    categories = []
    for row in soup.css.select('#pageContent div.table-rwd > div.tbody > div.tr'):
        cat_id = int(row.select_one('input[name="num"]')['value'])
        name = row.select_one('div.td[aria-label="領域類別"]').string.strip()
        last_updated = parse_date(row.select_one('div.td[aria-label="更新日期"]').string.strip())
        data_url = urljoin(NAER_BASE_URL, row.select_one('a[title="下載"]')['href'])

        categories.append(Category(category_id=cat_id, name=name, last_updated=last_updated, data_url=data_url))

    return categories


def print_usage():
    print('Usage: src/load_categories.py [-]')


if __name__ == '__main__':
    if '--help' in sys.argv:
        print_usage()
    else:
        file = sys.stdout if '-' in sys.argv else open(os.path.join('data', 'categories.csv'), 'w+')
        categories = download_categories()
        with file as f:
            save(file, categories)
