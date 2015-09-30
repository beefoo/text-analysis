# -*- coding: utf-8 -*-

# This script analyzes the text of Moby Dick by emotion, sentiment, subjectivity, and orientation

import csv
import json
import re
import sys

DATA_FILE = 'data/moby_dick_esso.csv'

chapters = []

# Read vocabulary
with open(DATA_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    for row in rows:
        entry = {}
        for i, h in enumerate(headers):
            entry[h] = row[i]
        entry['chapter'] = int(entry['chapter'])
        if len(chapters) < entry['chapter']:
            chapters.append([entry])
        else:
            chapters[entry['chapter']-1].append(entry)
