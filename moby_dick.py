# -*- coding: utf-8 -*-

# This script analyzes the text of Moby Dick by emotion, sentiment, subjectivity, and orientation

import csv
import json
import re
import sys

LEXICON_FILE = 'lexicons/lexicons_esso.csv'
TEXT_FILE = 'texts/moby_dick.txt'
DATA_FILE = 'data/moby_dick_esso.csv'
CHAPTER_FILE = 'data/moby_dick_chapters.json'

vocabulary = []

# Read vocabulary
with open(LEXICON_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    for row in rows:
        entry = {}
        for i, h in enumerate(headers):
            entry[h] = row[i]
        vocabulary.append(entry)

# Read text
punctuation_pattern = '[^a-z\-\. ]'
chapter_pattern = 'CHAPTER [1-9][0-9]*\. ([^\.]+)\.|(Epilogue)'
end_pattern = 'End of Project Gutenberg.*'
chapters = []
data = []
current_chapter = -1
current_paragraph = -1
current_sentence = -1

def addData(word):
    global data
    global vocabulary
    global current_chapter
    global current_paragraph
    global current_sentence

    emotion = -1
    sentiment = -1
    subjectivity = -1
    orientation = -1

    if len(word) > 5:
        data.append([emotion, sentiment, subjectivity, orientation, current_chapter, current_paragraph, current_sentence])


with open(TEXT_FILE, 'rb') as f:
    for line in f:
        line = line.strip()

        # Check for chapter match
        chapter_match = re.search(chapter_pattern, line)
        if chapter_match:
            chapter_name = chapter_match.group(1)
            if not chapter_name:
                chapter_name = chapter_match.group(2)
            chapters.append(chapter_name)
            current_chapter = len(chapters)
            current_paragraph = -1
            current_sentence = -1
            print "Chapter " + str(current_chapter) + ": " + chapter_name

        # Didn't reach the first chapter yet, just continue
        elif current_chapter < 0:
            continue

        else:
            # If end of book found, stop reading
            end_match = re.search(end_pattern, line)
            if end_match:
                break

            # Check for paragraph
            elif not line and current_sentence >= 0:
                current_paragraph += 1
                current_sentence = -1

            # Parse line
            elif line:
                current_paragraph = max(current_paragraph, 0)
                current_sentence = max(current_sentence, 0)
                line = line.lower() # lowercase
                line = re.sub(punctuation_pattern, ' ', line) # remove punctuation
                words = line.split()
                for word in words:
                    if '.' in word:
                        word = word.replace('.','')
                        addData(word)
                        current_sentence += 1
                    else:
                        addData(word)

# Output chapters as json
with open(CHAPTER_FILE, 'w') as outfile:
    json.dump(chapters, outfile)
    print('Successfully wrote '+str(len(chapters))+' chapters to file: '+CHAPTER_FILE)

# Output data as csv
with open(DATA_FILE, 'wb') as f:
    cw = csv.writer(f)
    cw.writerow(['emotion', 'sentiment', 'subjectivity', 'orientation', 'chapter', 'paragraph', 'sentence'])
    for entry in data:
        cw.writerow(entry)
    print('Successfully wrote '+str(len(data))+' entries to file: '+DATA_FILE)
