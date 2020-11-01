#!/usr/bin/env bash
scripts/get_term_categories.py > raw_data/categories.csv
scripts/download_terms.py 331
scripts/html_to_csv.py raw_data/html/Term_331_0.html > raw_data/csv/331.csv
