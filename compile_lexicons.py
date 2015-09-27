# -*- coding: utf-8 -*-

import csv

words = []
emotions = ['anger', 'fear', 'anticipation', 'trust', 'surprise', 'sadness', 'joy', 'disgust']
sentiments = ['positive', 'negative']
orientations = ['active', 'passive']
subjectivities = ['weak', 'strong']
default_word = {
    'emotion': '',
    'sentiment': '',
    'subjectivity': '',
    'orientation': '',
    'source': ''
}

def add_word(_w):
    global words

    matches = [w for w in words if w['word']==_w['word']]
    if len(matches):
        match = matches[0]
        for key in match:
            if not match[key] and _w[key]:
                words[match['index']][key] = _w[key]
    else:
        word = _w
        word['index'] = len(words)
        words.append(word)

# NRC Emotion Lexicon: http://www.saifmohammad.com/WebPages/lexicons.html
#   Format: aback \t anger \t 0
EMOLEX_FILE = "lexicons_external/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"

with open(EMOLEX_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter='\t')
    for _word, _category, _association in rows:
        word = default_word
        word['word'] = _word
        word['index'] = len(words)
        word['source'] = 'emolex'
        if category in emotions:
            word['emotion'] = category
        elif category in sentiments:
            word['sentiment'] = category
        words.append(word)

# Bing Liu's Opinion Lexicon: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon
OPINION_LEX_NEG_FILE = "lexicons_external/opinion-lexicon-English/negative-words.txt"
OPINION_LEX_POS_FILE = "lexicons_external/opinion-lexicon-English/positive-words.txt"

opinion_words = []

with open(OPINION_LEX_NEG_FILE) as f:
    negative_words = f.read().splitlines()
    for w in negative_words:
        word = default_word
        word['word'] = w
        word['sentiment'] = 'negative'
        word['source'] = 'opinion'
        add_word(word)

with open(OPINION_LEX_POS_FILE) as f:
    positive_words = f.read().splitlines()
    for w in positive_words:
        word = default_word
        word['word'] = w
        word['sentiment'] = 'positive'
        word['source'] = 'opinion'
        add_word(word)

# MPQA Subjectivity Lexicon: http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
#   Format: type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
#       type: strongsubj, weaksubj
#       pos1: adj, adverb, anypos, noun, verb
#       stemmed1: y, n
#       priorpolarity: positive, negative, both, neutral
MPQA_FILE = "lexicons_external/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff"

with open(MPQA_FILE) as f:
    lines = f.read().splitlines()
    for line in lines:
        pairs = line.split(" ")
        word = default_word
        word['source'] = 'mpqa'
        for pair in pairs:
            p = pair.split("=")
            key = p[0]
            if key=="type":
                word['subjectivity'] = p[1].replace('subj','')
            elif key=="word1":
                word['word'] = p[1]
            elif key=="priorpolarity" and p[1] in sentiments:
                word['sentiment'] = p[1]
        add_word(word)


# Harvard General Inquirer: http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm
#   Categories: http://www.wjh.harvard.edu/~inquirer/homecat.htm
INQUIRER_FILE = "lexicons_external/inquirerbasic.csv"

valid_headers = ["Entry", "Positiv", "Negativ", "Active", "Passive"]

with open(INQUIRER_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # populate movies list
    for row in rows:
        word = default_word
        word['source'] = 'inquirer'
        for i, h in enumerate(headers):
            if h=="Entry":
                word['word'] = row[i].lower()
            elif h=="Positiv" and row[i]:
                word['sentiment'] = 'positive'
            elif h=="Negative" and row[i]:
                word['sentiment'] = 'negative'
            elif h=="Active" and row[i]:
                word['orientation'] = 'active'
            elif h=="Passive" and row[i]:
                word['orientation'] = 'passive'
        add_word(word)
