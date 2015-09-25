# -*- coding: utf-8 -*-

import csv
import sys

# NRC Emotion Lexicon: http://www.saifmohammad.com/WebPages/lexicons.html
EMOLEX_FILE = "lexicons_external/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
# Read data from csv
with open(EMOLEX_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter='\t')
    for word, category, association in rows:
        association = int(association)

# Bing Liu's Opinion Lexicon: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon
OPINION_LEX_NEG_FILE = "lexicons_external/opinion-lexicon-English/negative-words.txt"
OPINION_LEX_POS_FILE = "lexicons_external/opinion-lexicon-English/positive-words.txt"

# MPQA Subjectivity Lexicon: http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
MPQA_FILE = "lexicons_external/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff"

# Harvard General Inquirer: http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm
INQUIRER_FILE = "lexicons_external/inquirerbasic.csv"
