# -*- coding: utf-8 -*-

# This script retrieves data from normalized text file based on lexicons
#   Usage: python get_data.py output/moby_dick_normal.json output/moby_dick_data.csv

import csv
import json
import sys

# Files
LEXICON_FILE = 'lexicons/lexicons_compiled.csv'
CATEGORIES_FILE = 'data/categories.json'

# Input
if len(sys.argv) < 2:
    print "Usage: %s <inputfile normal text json> <outputfile data csv>" % sys.argv[0]
    sys.exit(1)

TEXT_FILE = sys.argv[1]
DATA_FILE = sys.argv[2]

# Init
vocabulary = []
words = []
categories = {}
category_headers = []
text = {}
data = []
chapters = []

# Read vocabulary
with open(LEXICON_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    for row in rows:
        entry = {}
        for i, h in enumerate(headers):
            entry[h] = row[i]
        vocabulary.append(entry)
    words = [v['word'] for v in vocabulary]

# Read categories
with open(CATEGORIES_FILE) as f:
    categories = json.load(f)
    category_headers = categories.keys()

# Read normalized text
with open(TEXT_FILE) as f:
    text = json.load(f)
    chapters = text['chapters']

# Check if word matches any lexicons
def addData(word, chapter):
    global data
    global vocabulary
    global categories
    global category_headers
    global words

    match = -1
    for i,w in enumerate(words):
        if w==word:
            match = i
            break

    if match >= 0:
        entry = vocabulary[match]
        row = []
        for category in category_headers:
            if entry[category]:
                row.append(categories[category].index(entry[category]))
            else:
                row.append(-1)
        row.append(chapter)
        data.append(row)

# Read each chapter
for i, chapter in enumerate(chapters):
    print "Analyzing Chapter " + str(i+1) + ": " + chapter['title']
    words = chapter['text'].split(' ')
    for word in words:
        addData(word, i)

# Output data as csv
with open(DATA_FILE, 'wb') as f:
    cw = csv.writer(f)
    headers = category_headers
    headers.append('chapter')
    cw.writerow(headers)
    for row in data:
        cw.writerow(row)
    print('Successfully wrote '+str(len(data))+' entries to file: '+DATA_FILE)
