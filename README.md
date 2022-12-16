# theaconf-nlp

This repository is a collection different ways to analyse the the text (mostly abstracts) from the website of the 2022 Gesellschaft für Theaterwissenschaft congress "Matters Of Urgency": https://matters-of-urgency.de/

## get started:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Data

The first step before being able to work with the data is aquiring the -- in this case -- complete website as html files. One of the most straight forward ways to do this is using the commandline tool wget: https://www.gnu.org/software/wget/ or (german): https://wiki.ubuntuusers.de/wget/

In this case the complete command was: `wget -r -k -E -l 8 https://matters-of-urgency.de/`

This dumps the webite as functional html pages directly into the working folder.

## Parsing the HTML

The python library Beautiful Soup is used to parse all relevant text out of the HTML files. (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Unfortunately non-breaking space characters '&nbsp;' are not resolved completely, so I used 'unicodedata.normalize' additionally.

## Working with the texts

Not all abstracts share the same language, the big majority is german (40), two are english and four are mixed with parts in both, german and english. Because the english parts are so few and I am looking for comprehensive analyses over all the texts I translated the english parts manually with DeepL. (https://www.deepl.com/translator). This way I can treat all texts the same, only have to work with german spaCy models and get frequency counts that incorporate all texts.

### Frequency list

To create a frequency list of all the abstracts, each text is processed through the pretrained spaCy nlp pipeline for german (https://spacy.io/models/de#de_core_news_sm). Through that it's possible to extract each words lemma and build a list of all lemmas which is then counted for frequencies. To get only relevant words it's important to weed out stopwords -- unnecessary words that don't carry meaning but occur very often (e.g. "der", "werden", "in"). To do that built-in stopword lists from the nltk library (https://www.nltk.org/index.html) are used for german and english. 

### Wordcloud

A colourful visualisation of word frequencies is a wordcloud, in this case created with a wordcloud library for python. (https://pypi.org/project/wordcloud/) dimensions and scaling for the image can be controlled directly in the script.

## This Repository:

abstracts folder: all abstracts as html files

matter-of-urgency.de folder: all html pages from the website as dump

11_test.txt: contexts for 11 most common words

abstracts_processing.py: Python script to work with everything

just-texts.txt: all plain text from all abstracts

figure.png: wordcloud picture

praktik_sentences.txt: All sentences with "Praktik"

praktik_title.txt: All titles from abstracs containing the word "Praktik" 

requirements.txt: list of requirements for this repository
