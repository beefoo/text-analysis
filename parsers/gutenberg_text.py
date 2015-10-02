# -*- coding: utf-8 -*-

# This script normalizes Gutenberg text
#   Usage: gutenberg_text.py ../texts/moby_dick.txt ../output/moby_dick_normal.json ../output/moby_dick_chapters.json

import json
import re
import sys

# Input
if len(sys.argv) < 3:
    print "Usage: %s <text file> <output text json file> <output chapter json file>" % sys.argv[0]
    sys.exit(1)

# Files
TEXT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
CHAPTERS_FILE = sys.argv[3]

# Text patterns
punctuation_pattern = '[^a-z\- ]|\-\-'
title_pattern = '^Title: (.+)'
author_pattern = '^Author: (.+)'
chapter_pattern = '^CHAPTER [1-9IVX][0-9IVX]*\.? ([^.]+)\.?$|^(Epilogue)$'
end_pattern = 'End of Project Gutenberg.*'

# Init data
data = {
    'title': '',
    'author': ''
}
chapters = []

with open(TEXT_FILE, 'rb') as f:
    for line in f:
        line = line.strip()

        # Check for chapter match
        chapter_match = re.search(chapter_pattern, line)
        if chapter_match:
            chapter_name = chapter_match.group(1)
            if not chapter_name:
                chapter_name = chapter_match.group(2)
            chapters.append({
                'title': chapter_name,
                'text': ''
            })
            print "Chapter " + str(len(chapters)) + ": " + chapter_name

        # Didn't reach the first chapter yet, check for title and author, and continue
        elif not len(chapters):
            # Check for title
            if not data['title']:
                title_match = re.search(title_pattern, line)
                if title_match:
                    data['title'] = title_match.group(1)
            # Check for author
            if not data['author']:
                author_match = re.search(author_pattern, line)
                if author_match:
                    data['author'] = author_match.group(1)
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
