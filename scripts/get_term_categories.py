#!/usr/bin/env python

import re
import requests
import sys

NAER_INDEX_URL = 'http://terms.naer.edu.tw/download/'

def load_categories():
    with requests.get(NAER_INDEX_URL) as r:
        response = r.text

    pattern = re.compile(r'<a href="/download/(?P<id>\d+)/" title="最後修改 (?P<last_updated>[\d \-\:]+)">(?P<name>[^<]+)</a>')
    categories = []
    for match in pattern.finditer(response):
        categories.append(match['id'])
        print(match['id'], match['name'], match['last_updated'], sep=',')

    return categories

def show_empty_categories():
    with requests.get(NAER_INDEX_URL) as r:
        response = r.text

    # Bonus: warns about categories without files
    empty_pattern = re.compile(r'<a href="" title="沒有檔案" onclick="return false;">(?P<name>[^<]+)</a>')
    for match in empty_pattern.finditer(response):
        print('WARN: No file provided by', match['name'], file=sys.stderr)

if __name__ == '__main__':
    load_categories()
    # Categories without available file to download are only the names of
    # non-Anglosphere Nobel prize winners for now; so we are not printing them
    # at this point.
