#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree

input = sys.stdin


tree = ET.fromstring(input.read())
terms = tree.findall('WORD_PAIRS_DATA')

for term in terms:
    print (term.attrib)
