#!/usr/bin/env python

import re
import requests
import sys

NAER_INDEX_URL = 'http://terms.naer.edu.tw/download/'

def main():
    with requests.get(NAER_INDEX_URL) as r:
        response = r.text

    pattern = re.compile(r'<a href="/download/(?P<id>\d+)/" title="最後修改 (?P<last_updated>[\d \-\:]+)">(?P<name>[^<]+)</a>')
    for match in pattern.finditer(response):
        print(match['id'], match['name'], match['last_updated'], sep=',')

    # Bonus: warns about categories without files
    empty_pattern = re.compile(r'<a href="" title="沒有檔案" onclick="return false;">(?P<name>[^<]+)</a>')
    for match in empty_pattern.finditer(response):
        print('WARN: No file provided by', match['name'], file=sys.stderr)

if __name__ == '__main__':
    main()
