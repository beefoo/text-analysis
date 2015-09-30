# -*- coding: utf-8 -*-

# This script analyzes text data based on lexicons
#   Usage: python analyze_data.py output/moby_dick_data.csv output/moby_dick_analysis.json 400 200

import csv
import json
import sys

# Files
CATEGORIES_FILE = 'data/categories.json'

# Input
if len(sys.argv) < 4:
    print "Usage: %s <data csv file> <a path to output json file> <word buffer> <word offset>" % sys.argv[0]
    sys.exit(1)

DATA_FILE = sys.argv[1]
ANALYSIS_FILE = sys.argv[2]
WORD_BUFFER_SIZE = int(sys.argv[3])
WORD_OFFSET = int(sys.argv[4])

# Init
categories = {}
input_data = []
max_values = {}
data = []

# Read categories
with open(CATEGORIES_FILE) as f:
    categories = json.load(f)

# Init max
for c in categories:
    max_values[c] = []
    for cc in categories[c]:
        max_values[c].append(0)

# Read data file
with open(DATA_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    for row in rows:
        entry = {}
        for i, h in enumerate(headers):
            entry[h] = int(row[i])
        input_data.append(entry)

# Analyze a list of words
def do_analysis(word_list, chapter):
    global categories
    global data
    global max_values

    entry = {
        'chapter': chapter
    }

    # Initilize entry
    for c in categories:
        entry[c] = []
        for cc in categories[c]:
            entry[c].append(0)

    # Increment counts
    for w in word_list:
        for c in categories:
            if w[c] >= 0:
                entry[c][w[c]] += 1
                # Track max values
                if entry[c][w[c]] > max_values[c][w[c]]:
                    max_values[c][w[c]] = entry[c][w[c]]

    # Add data
    data.append(entry)

# Analayze data
current_chapter = 0
word_buffer = []
for entry in input_data:

    # New chapter found
    if entry['chapter'] > current_chapter:
        print 'Finished Chapter ' + str(current_chapter+1)
        current_chapter = entry['chapter']
        do_analysis(word_buffer, current_chapter)
        word_buffer = [entry]

    # Buffer size reached, do analysis
    elif len(word_buffer) >= WORD_BUFFER_SIZE:
        do_analysis(word_buffer, current_chapter)
        word_buffer = word_buffer[WORD_OFFSET:] # first <WORD_OFFSET> from buffer

    # Buffer not large enough, add entry
    else:
        word_buffer.append(entry)

# Process remaining buffer
do_analysis(word_buffer, current_chapter)
print 'Finished Chapter ' + str(current_chapter+1)

# Normalize data
for i, entry in enumerate(data):
    for c in categories:
        for j,v in enumerate(entry[c]):
            data[i][c][j] = round(1.0 * v / max_values[c][j], 3)

# Output analysis as json
with open(ANALYSIS_FILE, 'w') as f:
    json.dump(data, f)
    print('Successfully wrote '+str(len(data))+' entries to file: '+ANALYSIS_FILE)
