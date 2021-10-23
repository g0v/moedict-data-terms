#!/usr/bin/env python

import re
import sys
from enum import Enum

def convert(filename: str):
    # Read the whole file into string buffer
    with open(filename, 'r') as f:
        s = f.read()
    buf = sys.stdout

    pattern = re.compile(r'<(?P<name>/?[A-Za-z]+)[^>]*>')
    td_tag_tail = None
    need_comma = False

    for matched_tag in pattern.finditer(s):
        if td_tag_tail is not None:     # </td>
            assert matched_tag['name'] == '/td'

            # Close the tag and extract the content
            content = s[td_tag_tail:matched_tag.start()]
            content = content.replace('\n', ' ').strip()

            # Quote the content if necessary
            if ' ' in content:
                buf.write('"')
                buf.write(content)
                buf.write('"')
            else:
                buf.write(content)

            # Clear state
            td_tag_tail = None
            need_comma = True

        elif matched_tag['name'] == 'td':
            td_tag_tail = matched_tag.end()
            # Write comma if needed
            if need_comma:
                buf.write(',')

        elif matched_tag['name'] == '/tr':
            buf.write('\n')
            need_comma = False

    buf.flush()


def print_usage():
    print('Usage: html_to_csv.py <filename>')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
    else:
        convert(sys.argv[1])
