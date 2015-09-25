
NRC Word-Colour Association Lexicon
(NRC Colour Lexicon)
Version 0.92
21 July 2011
Copyright (C) 2011 National Research Council Canada (NRC)
Contact: Saif Mohammad (saif.mohammad@nrc-cnrc.gc.ca)

Terms of use:
1. This lexicon can be used freely for research purposes. 
2. The papers listed below provide details of the creation and use of 
   the lexicon. If you use a lexicon, then please cite the associated 
   papers.
3. If interested in commercial use of the lexicon, send email to the 
   contact. 
4. If you use the lexicon in a product or application, then please 
   credit the authors and NRC appropriately. Also, if you send us an 
   email, we will be thrilled to know about how you have used the 
   lexicon.
5. National Research Council Canada (NRC) disclaims any responsibility 
   for the use of the lexicon and does not provide technical support. 
   However, the contact listed above will be happy to respond to 
   queries and clarifications.
6. Rather than redistributing the data, please direct interested 
   parties to this page:
   http://www.purl.com/net/lexicons 

Please feel free to send us an email:
- with feedback regarding the lexicon. 
- with information on how you have used the lexicon. 
- if interested in having us analyze your data for colour, sentiment, 
  emotion, and other affectual information.
- if interested in a collaborative research project.

.......................................................................

NRC WORD-COLOUR ASSOCIATION LEXICON
-----------------------------------
Many real-world concepts have associations with colours. For example,
iceberg is associated with white, vegetation with green, danger with
red, and so on.  The NRC word-colour association lexicon is a list of
words and the colours they are most associated with.  The annotations
were manually done through Amazon's Mechanical Turk. Refer to
publications below for more details.

.......................................................................

PUBLICATIONS
------------
Details of the lexicon can be found in the following peer-reviewed
publications:

-- Colourful Language: Measuring Word-Colour Associations, Saif
Mohammad, In Proceedings of the ACL 2011 Workshop on Cognitive
Modeling and Computational Linguistics (CMCL), June 2011, Portland,
OR.

-- Even the Abstract have Colour: Consensus in WordColour
Associations, Saif Mohammad, In Proceedings of the 49th Annual Meeting
of the Association for Computational Linguistics: Human Language
Technologies, June 2011, Portland, OR.

Links to the papers are available here:
http://www.purl.org/net/saif.mohammad/research
.......................................................................

VERSION INFORMATION
-------------------
Version 0.92 is the latest version as of 21 July 2011. 

.......................................................................

FORMAT
------
Each line has the following format:
$TargetWord--$Sense<tab>Colour=$Colour<tab>VotesForThisColour=$VotesForThisColour    TotalVotesCast=$TotalVotesCast

-- $TargetWord is a word for which the annotators provided colour associations.

-- $Sense is one or more comma-separated words that indicate the sense of
the target word for which the annotations are provided.

-- $Colour is the colour most associated with the target word. It is one of eleven colours---white, black, red, green, yellow, blue, brown, pink, purple, orange, grey.
If each of the annotators suggested a different colour association for the target word, then $Colour is set to None.

-- $VotesForThisColour is the number of annotators who chose $Colour for the target word.
It is set to None if $Colour is None.

-- $TotalVotesCast is the total number of annotators who gave colour associations for the target word.

.......................................................................

CONTACT INFORMATION
-------------------
Saif Mohammad
Research Officer, National Research Council Canada
email: saif.mohammad@nrc-cnrc.gc.ca
phone: +1-613-993-0620

.......................................................................
