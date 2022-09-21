import collections
import json
import os
import unicodedata

import nltk
import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

#initialise text for lists
text_list = []
all_abstracts = {}
just_texts = []
all_words = []
 
directory = "abstracts/deutsch"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    with open(f, encoding="utf-8") as f:
        #reading file contents into the string "html"
        html = f.read()#.decode("utf-8", "ignore")
        
        temp_list = []
        
        #using beautiful soup to parse the document
        soup = BeautifulSoup(html, "html.parser")
        
        raw_title = soup.find("h1")
        
        title = raw_title.get_text()
        
        #print(title)
        
        raw_paragraphs = soup.find_all("p")
        
        for raw_para in raw_paragraphs:
            para = raw_para.get_text()
            
            temp_list.append(para)
            
        #print(temp_list)
        
        abstract_para = max(temp_list, key=len)
        
        just_texts.append(unicodedata.normalize("NFKD", abstract_para))
          
        all_abstracts[title] = temp_list
            
        
        pass
            #print(text)
            
        print(just_texts)


stopw = set(stopwords.words("german"))
enstopw = set(stopwords.words("english"))

nlp = spacy.load("de_core_news_sm")   

for textelment in just_texts:
    nlptext = nlp(textelment)
    
    for wordelemt in nlptext:
        lemma = wordelemt.lemma_
        if lemma not in stopw and lemma not in enstopw and lemma != "--" and lemma != "’":
            all_words.append(lemma)
     
#for elem in all_words:
#    if elem 

freqcounter = collections.Counter(all_words)

print(freqcounter.most_common(40))

with open("just-texts.txt", "w") as g:
    for i in just_texts:
        g.write(i)


#a = just_texts[1]
#b = nlp(a)
#
#for c in b:
#    print(c.lemma_)


#for key,value in all_abstracts.items():
    #print(key, value)
    
