# -*- coding: utf-8 -*-

# This script compiles and normalizes a number of emotion-sentiment-subjectivity-orientation lexicons from different sources

import csv
import json
import sys

# Files
OUTPUT_FILE = "lexicons/lexicons_compiled.csv"
CATEGORIES_FILE = "data/categories.json"

# Init
words = []
match_count = 0
add_count = 0
categories = {}

# Read categories
with open(CATEGORIES_FILE) as f:
    categories = json.load(f)

# Init headers
category_headers = categories.keys()
headers = ['word']
headers.extend(category_headers)
headers.append('source')

# Adds new word or extends exisiting word
def add_word(_w):
    global words
    global match_count
    global add_count
    global headers

    matches = [w for w in words if w['word'] == _w['word']]

    if len(matches) > 0:
        match = matches[0]
        for key in match:
            if not match[key] and key in _w and _w[key]:
                words[match['index']][key] = _w[key]
        match_count += 1
    else:
        word = _w
        word['index'] = len(words)
        for h in headers:
            if h not in word:
                word[h] = ""
        words.append(word)
        add_count += 1

# NRC Emotion Lexicon: http://www.saifmohammad.com/WebPages/lexicons.html
#   Format: aback \t anger \t 0
EMOLEX_FILE = "lexicons_external/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
match_count = 0
add_count = 0

with open(EMOLEX_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter='\t')
    for _word, _category, _association in rows:
        word = {}
        word['word'] = _word.decode('utf-8').lower()
        word['source'] = 'emolex'
        if _category in categories['emotion']:
            word['emotion'] = _category
        elif _category in categories['sentiment']:
            word['sentiment'] = _category
        if int(_association) > 0:
            add_word(word)

print "Emolex matches: " + str(match_count) + ", added: " + str(add_count)

# Bing Liu's Opinion Lexicon: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon
OPINION_LEX_NEG_FILE = "lexicons_external/opinion-lexicon-English/negative-words.txt"
OPINION_LEX_POS_FILE = "lexicons_external/opinion-lexicon-English/positive-words.txt"
match_count = 0
add_count = 0

with open(OPINION_LEX_NEG_FILE) as f:
    negative_words = f.read().splitlines()
    for w in negative_words:
        word = {}
        word['word'] = w.decode('utf-8').lower()
        word['sentiment'] = 'negative'
        word['source'] = 'opinion'
        add_word(word)

with open(OPINION_LEX_POS_FILE) as f:
    positive_words = f.read().splitlines()
    for w in positive_words:
        word = {}
        word['word'] = w.decode('utf-8').lower()
        word['sentiment'] = 'positive'
        word['source'] = 'opinion'
        add_word(word)

print "Opinion Lexicon matches: " + str(match_count) + ", added: " + str(add_count)

# MPQA Subjectivity Lexicon: http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
#   Format: type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
#       type: strongsubj, weaksubj
#       pos1: adj, adverb, anypos, noun, verb
#       stemmed1: y, n
#       priorpolarity: positive, negative, both, neutral
MPQA_FILE = "lexicons_external/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff"
match_count = 0
add_count = 0

with open(MPQA_FILE) as f:
    lines = f.read().splitlines()
    for line in lines:
        pairs = line.split(" ")
        word = {}
        word['source'] = 'mpqa'
        for pair in pairs:
            p = pair.split("=")
            key = p[0]
            if key=="type":
                subjectivity = p[1].replace('subj','')
                if subjectivity in categories['subjectivity']:
                    word['subjectivity'] = subjectivity
            elif key=="word1":
                word['word'] = p[1].decode('utf-8').lower()
            elif key=="priorpolarity" and p[1] in categories['sentiment']:
                word['sentiment'] = p[1]
        if word['word'] and ('subjectivity' in word or 'sentiment' in word):
            add_word(word)
        else:
            print "MPQA warning: no match for " + word['word']

print "MPQA matches: " + str(match_count) + ", added: " + str(add_count)

# Harvard General Inquirer: http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm
#   Categories: http://www.wjh.harvard.edu/~inquirer/homecat.htm
INQUIRER_FILE = "lexicons_external/inquirerbasic.csv"
match_count = 0
add_count = 0

with open(INQUIRER_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    _headers = next(rows, None) # remove header
    # populate movies list
    for row in rows:
        word = {}
        word['source'] = 'inquirer'
        for i, h in enumerate(_headers):
            if h=="Entry":
                word['word'] = row[i].decode('utf-8').lower()
                if '#' in word['word']:
                    word['word'] = word['word'].split('#')[0]
            elif h=="Positiv" and row[i]:
                word['sentiment'] = 'positive'
            elif h=="Negative" and row[i]:
                word['sentiment'] = 'negative'
            elif h=="Active" and row[i]:
                word['orientation'] = 'active'
            elif h=="Passive" and row[i]:
                word['orientation'] = 'passive'
        if word['word'] and ('sentiment' in word or 'orientation' in word):
            add_word(word)

print "Inquirer matches: " + str(match_count) + ", added: " + str(add_count)

# NRC Word-Colour Association Lexicon: http://www.saifmohammad.com/WebPages/lexicons.html
#   Format: motive--motion \t Colour=black \t VotesForThisColour=2 \t TotalVotesCast=4
COLOR_FILE = "lexicons_external/NRC-Colour-Lexicon-v0.92/NRC-color-lexicon-senselevel-v0.92.txt"
match_count = 0
add_count = 0

with open(COLOR_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter='\t')
    for _word_sense, _color, _votes, _votes_total in rows:
        word = {}
        word['word'] = _word_sense.split("--")[0].decode('utf-8').lower()
        word['color'] = _color.split("=")[1]
        word['source'] = 'colour'
        votes = _votes.split("=")[1]
        votes_total = _votes_total.split("=")[1]
        if votes.isdigit() and votes_total.isdigit() and word['color'] in categories['color'] and float(votes_total) and float(votes) / float(votes_total) > 0.5:
            add_word(word)

print "Colour matches: " + str(match_count) + ", added: " + str(add_count)

# Sort and report
words = sorted(words, key=lambda k: k['word'])
word_count = len(words)
print "Total word count: " + str(word_count)
for ch in category_headers:
    words_with_category = len([w for w in words if w[ch]])
    print "Words with "+ch+": " + str(words_with_category) + " (" + str(round(1.0*words_with_category/word_count*100, 1)) + "%)"

# Output snapshot 2015-09-30
#
# Emolex matches: 7433, added: 6468
# Opinion Lexicon matches: 2490, added: 4298
# MPQA matches: 7225, added: 997
# Inquirer matches: 3529, added: 853
# Colour matches: 4385, added: 2236
# Total word count: 14852
# Words with emotion: 4463 (30.0%)
# Words with sentiment: 10916 (73.5%)
# Words with subjectivity: 6886 (46.4%)
# Words with orientation: 2192 (14.8%)
# Words with color: 5404 (36.4%)

# Output as csv
with open(OUTPUT_FILE, 'wb') as f:
    cw = csv.writer(f)
    cw.writerow(headers)
    for w in words:
        row = []
        for h in headers:
            if h=='word':
                w[h] = w[h].encode('utf-8')
            row.append(w[h])
        cw.writerow(row)
    print('Successfully wrote words to file: '+OUTPUT_FILE)
