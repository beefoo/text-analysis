# -*- coding: utf-8 -*-

# This script normalizes HTML files from http://www.ae-lib.org.ua/
#   Usage: ae_lib_html.py ../texts/the_hobbit.html ../output/hobbit_normal.json ../output/hobbit_chapters.json

import json
import re
import sys
from bs4 import BeautifulSoup

# Input
if len(sys.argv) < 3:
    print "Usage: %s <text file> <output text json file> <output chapter json file>" % sys.argv[0]
    sys.exit(1)

# Files
HTML_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
CHAPTERS_FILE = sys.argv[3]

# Text patterns
punctuation_pattern = '[^a-z\- ]|\-\-'
title_pattern = '^Title: (.+)'
author_pattern = '^Author: (.+)'
chapter_pattern = '^Chapter [1-9IVX][0-9IVX]*$'
end_pattern = '©.*'

# Init data
data = {
    'title': '',
    'author': ''
}
chapters = []
all_text = ""

# Parse HTML
with open(HTML_FILE, 'rb') as f:
    soup = BeautifulSoup(f.read(), "lxml")
    all_text = ''.join(soup.findAll(text=True))

lines = all_text.split('\n')
chapter_matched = False
for line in lines:
    line = line.strip()

    # Check for chapter match
    chapter_match = re.search(chapter_pattern, line)

    # Chapter was matched on the previous line; this is the chapter title
    if chapter_matched:
        chapters.append({
            'title': line,
            'text': ''
        })
        print "Chapter " + str(len(chapters)) + ": " + line
        chapter_matched = False

    # Found chapter, title is on the next line
    elif chapter_match:
        chapter_matched = True
        continue

    # Didn't reach the first chapter yet, check for title and author, and continue
    elif not len(chapters):
        continue

    else:
        # If end of book found, stop reading
        end_match = re.search(end_pattern, line)
        if end_match:
            break

        # Parse line
        elif line:
            line = line.lower() # lowercase
            line = re.sub(punctuation_pattern, ' ', line) # remove punctuation
            words = ' '.join(line.split()) # remove multi-space
            if not chapters[-1]['text']:
                chapters[-1]['text'] = words
            else:
                chapters[-1]['text'] += " " + words

# Output chapters as json
with open(CHAPTERS_FILE, 'w') as f:
    chapter_titles = [c['title'] for c in chapters]
    json.dump(chapter_titles, f)
    print('Successfully wrote '+str(len(chapters))+' chapters to file: '+CHAPTERS_FILE)

# Output data as json
with open(OUTPUT_FILE, 'w') as f:
    data['chapters'] = chapters
    json.dump(data, f)
    print('Successfully wrote '+str(len(chapters))+' chapters to file: '+OUTPUT_FILE)
