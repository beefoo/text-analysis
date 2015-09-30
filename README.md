# Scripts for analyzing text

Based on emotion, sentiment, subjectivity, orientation, and color.

## Lexicons Used

- [NRC Emotion Lexicon](http://www.saifmohammad.com/WebPages/lexicons.html)
- [Bing Liu's Opinion Lexicon](http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon)
- [MPQA Subjectivity Lexicon](http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/)
- [Harvard General Inquirer](http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm)
- [NRC Word-Colour Association Lexicon](http://www.saifmohammad.com/WebPages/lexicons.html)

These lexicons were parsed and compiled using the script [compile_lexicons.py](compile_lexicons.py) into file [lexicons/lexicons_compiled.csv](lexicons/lexicons_compiled.csv) using [these categories](data/categories.json) with the following counts:

- Total word count: _14,852_
- Words with emotion: _4,463 (30.0%)_
- Words with sentiment: _10,916 (73.5%)_
- Words with subjectivity: _6,886 (46.4%)_
- Words with orientation: _2,192 (14.8%)_
- Words with color: _5,404 (36.4%)_

## How to analyze text

1. Download text, e.g. [texts/moby_dick.txt](texts/moby_dick.txt)
2. Write a parser for text, e.g. [parsers/moby_dick.py](parsers/moby_dick.py) which outputs JSON file in format:

   ```javascript
   {
     "title": "Moby-Dick; or, The Whale'",
     "chapters": [
       {
         "title": "Loomings",
         "text": "discrete words in lowercase separated by spaces with punctuation removed"
       },
       {
         "title": "The Carpet-Bag",
         "text": "discrete words in lowercase separated by spaces with punctuation removed"
       },
       ...
     ]
   }
   ```

3. Run `get_data.py <json file from previous step> <a path to output csv file>`, e.g. `get_data.py data/moby_dick_normal.json output/moby_dick_data.csv`. This outputs a .csv file in the format:

   ```
   emotion,color,orientation,sentiment,subjectivity,chapter
   0,2,1,1,-1,0
   ...
   ```

   Where each row represents a word, and each column represent the index of each category listed in [data/categories.json](data/categories.json)

4. Run `analyze_data.py <csv file from previous step> <a path to output csv file> <word buffer> <word offset>`, e.g. `python analyze_data.py output/moby_dick_data.csv output/moby_dick_analysis.json 200 100`. This outputs a .json file in the format:

   ```javascript
   [
    {
      "chapter": 0,
      "emotion": [
        0.500, // anger
        0.250, // fear
        ...
      ],
      "subjectivity": [
        0.600, // weak
        0.150 // strong
      ],
      "sentiment": [
        0.750, // positive
        0.050 // negative
      ],
      "orientation": [
        0.850, // active
        0.450 // passive
      ],
      "color": [
        0.950, // white
        0.001, // black
        ...
      ]
    },
    ...
   ]
   ```

   Where each item represents a group of words (with a size of `word buffer` as configured in the previous step). The numbers are percentages between 0 and 1 that represents the relative weight of that particular category value.

5. Optionally, run `python report_data.py <analysis json file> <output dir>` to write individual .csv files for each category, e.g. `python report_data.py output/moby_dick_analysis.json output/moby_dick/`
