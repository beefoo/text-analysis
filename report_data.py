# -*- coding: utf-8 -*-

# This script analyzes text data based on lexicons
#   Usage: python report_data.py output/moby_dick_analysis.json output/moby_dick/

import csv
import json
import sys

# Files
CATEGORIES_FILE = 'data/categories.json'

# Input
if len(sys.argv) < 2:
    print "Usage: %s <analysis json file> <output dir>" % sys.argv[0]
    sys.exit(1)

ANALYSIS_FILE = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

# Init
categories = {}
data = []

# Read categories
with open(CATEGORIES_FILE) as f:
    categories = json.load(f)

# Read data
with open(ANALYSIS_FILE) as f:
    data = json.load(f)

# Write individual csv's for each category
for c in categories:
    # Output category as csv
    with open(OUTPUT_DIR + c + '.csv', 'wb') as f:
        cw = csv.writer(f)
        headers = categories[c]
        headers.append('chapter')
        cw.writerow(headers)
        for entry in data:
            row = entry[c]
            row.append(entry['chapter'])
            cw.writerow(row)
        print('Successfully wrote to file: '+OUTPUT_DIR + c + '.csv')
