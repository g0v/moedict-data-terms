#!/usr/bin/env bash
scripts/get_term_categories.py > raw_data/categories.csv
scripts/html_to_csv.py samples/Term_331_0.html > raw_data/331.csv
