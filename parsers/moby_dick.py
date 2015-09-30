# -*- coding: utf-8 -*-

# This script normalizes Moby Dick text

import json
import re
import sys

# Files
TEXT_FILE = '../texts/moby_dick.txt'
OUTPUT_FILE = '../output/moby_dick_normal.json'
CHAPTERS_FILE = '../output/moby_dick_chapters.json'

# Text patterns
punctuation_pattern = '[^a-z\- ]|\-\-'
chapter_pattern = 'CHAPTER [1-9][0-9]*\. ([^\.]+)\.|(Epilogue)'
end_pattern = 'End of Project Gutenberg.*'

# Init data
data = {
    'title': 'Moby-Dick; or, The Whale'
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

        # Didn't reach the first chapter yet, just continue
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
