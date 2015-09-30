# -*- coding: utf-8 -*-

# This script analyzes text data based on lexicons
#   Usage: python analyze_data.py output/moby_dick_data.csv output/moby_dick_analysis.json 200 100

import csv
import json
import sys

# Files
CATEGORIES_FILE = 'data/categories.json'

# Input
if len(sys.argv) < 4:
    print "Usage: %s <data csv file> <a path to output csv file> <word buffer> <word offset>`" % sys.argv[0]
    sys.exit(1)

DATA_FILE = sys.argv[1]
ANALYSIS_FILE = sys.argv[2]
WORD_BUFFER = int(sys.argv[3])
WORD_OFFSET = int(sys.argv[4])

# Init
categories = {}
category_headers = []

# Read categories
with open(CATEGORIES_FILE) as f:
    categories = json.load(f)
    category_headers = categories.keys()
