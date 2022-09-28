import collections
import json
from operator import contains
import os
import unicodedata

import nltk
import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import defaultdict
import pytextrank

#initialise text for lists
text_list = []
all_abstracts = {}
just_texts = []
all_words = []
 
 #specify directory with all relevant html pages
directory = "abstracts/deutsch"

#read all html files in the directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    with open(f, encoding="utf-8") as f:
        #reading file contents into the string "html"
        html = f.read()
        
        #temporary list for all paragraphs in one file
        temp_list = []
        
        #using beautiful soup to parse the document
        soup = BeautifulSoup(html, "html.parser")
        
        #find title tag for hi title
        raw_title = soup.find("h1")
        
        #get rid of html tags to have only text
        title = raw_title.get_text()
        
        #find all "p" tags with beautiful soup
        raw_paragraphs = soup.find_all("p")
        
        #extract only plain text from all "p" segments
        for raw_para in raw_paragraphs:
            para = raw_para.get_text()
            
            temp_list.append(para)
        
        #find the paragraph that contains the whole abstract text by picking the longest
        abstract_para = max(temp_list, key=len)
        
        #put the abstract paragraph in a list of all paragraphs, 
        #whilst normalising the encoding (specifically non breaking spaces)
        just_texts.append(unicodedata.normalize("NFKC", abstract_para))
        
        #put all paragraphs from the html in one dictionary with the title as key
        all_abstracts[title] = temp_list
        
        #print to debug   
        print(just_texts)

#write all plain text into an output file
with open("just-texts.txt", "w") as g:
    for i in just_texts:
        g.write(i)

#get stopword lists for english and german from NLTK toolkit
stopw = set(stopwords.words("german"))
enstopw = set(stopwords.words("english"))

#add relevant stopwords that were not included
add_stopw = ["für", "sowie", "über", "u", "innen", "inn"]

for i in add_stopw:
    stopw.add(i)


#### Create NLP model

#load pretrained spaCy nlp model for german
nlp = spacy.load("de_core_news_sm")  

nlp.add_pipe("textrank") 

phrases = []

#execute nlp pipeline for all texts
for textelment in just_texts:
    nlptext = nlp(textelment)
    
    #create a lemmatized list of all words that are neither stopwords nor punctuation
    for wordelemt in nlptext:
        lemma = wordelemt.lemma_
        if lemma not in stopw and lemma not in enstopw and lemma != "--" and lemma != "’":
            all_words.append(lemma)
    
    for phrase in nlptext._.phrases:
        phrases.append(phrase)

#count the frequency of every lemma
freqcounter = collections.Counter(all_words)

#debug: print most common 40 words
print(freqcounter.most_common(40))

#create a list of most common 11 words
mostcom_11 = freqcounter.most_common(11)
mostcom_11 = [word for word, count in mostcom_11]

#prepare defaultdict for the contexts of the most common 11 words
mostcom_11_contexts = defaultdict(list)

#prepare lists for sentences and abstracts that contain the word 'Praktik'
praktik_sents = []
praktik_title = []

#extract contexts for most common 11 and sentences for 'Praktik'
for abstract in just_texts:
    nlptext = nlp(abstract)
    
    #spaCy module senter automatically detects sentences saved in '.sents'
    for sent in nlptext.sents:
        for wordelemt in sent:
            
            #get lemma of every word
            lemma = wordelemt.lemma_
            if lemma in mostcom_11:
                
                #separate instances like "Insitute/Universitäten"
                sent1 = sent.text.replace('/', ' ')
                
                #split sentence into list of singular words
                sent1 = sent1.split(" ")
                
                #get rid of punctuation on words
                sent1 = [word.strip(',.?!():;"„“ ‘') for word in sent1]
                
                #get string of relevant word
                word1 = wordelemt.text
                
                #get index of relevant word
                i = sent1.index(word1)
                
                #extract context ba getting 5 words before and after 
                # the relevant word in the sentence
                context = sent1[max(i - 5, 0):i+5]
                
                #save context in dictionary with lemma as key
                mostcom_11_contexts[lemma].append(' '.join(context))
                pass
            
            #get all sentences with 'Praktik'
            if lemma == "Praktik":
                praktik_sents.append(sent)
            
#save all contexts into output file
with open("11_test.txt", "w", encoding="utf-8") as h:
    for key, values in mostcom_11_contexts.items():
        h.write(f'\n {key}: \n')
        for value in values:
            h.write(f'{value} \n')

#get all titles of abstracts with 'Praktik' sentences
for title, abstract in all_abstracts.items():
    for sen in praktik_sents:
        for elem in abstract:
            if sen.text in elem:
                praktik_title.append(title)
   
#write all 'Praktik' sentences into file
with open("praktik_sentences.txt", "w", encoding="utf-8") as j:
    for sen in praktik_sents:
        j.write(f'{sen} \n')

#write all abstract titles for 'Praktik' into file
with open("praktik_title.txt", "w", encoding="utf-8") as k:
    for title in praktik_title:
        k.write(f'{title} \n')




#### Create Wordcloud

#create one string of all abstracts
text = ' '.join(all_words)

#check binary representation of the words
#for word in mostcom_11:
#    hexwords = ':'.join(hex(ord(x))[2:] for x in word )
#    print(word)
#    print(hexwords)
#
#print(type(text))


# Generate a word cloud image
wordcloud = WordCloud(width=4000, height=2000).generate(text)

#save wordcloud as png
wordcloud.to_file("figure.png")

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(width=2000, height=1000, max_font_size=60).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

