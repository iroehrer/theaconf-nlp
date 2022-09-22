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
        
with open("just-texts.txt", "w") as g:
    for i in just_texts:
        g.write(i)

stopw = set(stopwords.words("german"))
enstopw = set(stopwords.words("english"))

add_stopw = ["für", "sowie", "über", "u"]

#stopw.add("für")

#
for i in add_stopw:
    stopw.add(i)

nlp = spacy.load("de_core_news_sm")   

for textelment in just_texts:
    nlptext = nlp(textelment)
    
    for wordelemt in nlptext:
        lemma = wordelemt.lemma_
        if lemma not in stopw and lemma not in enstopw and lemma != "--" and lemma != "’":
            all_words.append(lemma)

freqcounter = collections.Counter(all_words)

print(freqcounter.most_common(40))



mostcom_11 = freqcounter.most_common(11)
mostcom_11 = [word for word, count in mostcom_11]

mostcom_11_contexts = defaultdict(list)

for abstract in just_texts:
    nlptext = nlp(abstract)
    
    for sent in nlptext.sents:
        for wordelemt in sent:
            lemma = wordelemt.lemma_
            if lemma in mostcom_11:
                sent1 = sent.text.replace('/', ' ')
                sent1 = sent1.split(" ")
                sent1 = [word.strip(',.?!():;"„“ ') for word in sent1]
                word1 = wordelemt.text
                i = sent1.index(word1)
                
                context = sent1[max(i - 5, 0):i+5]
                
                mostcom_11_contexts[lemma].append(' '.join(context))
                pass
            

with open("11_test.txt", "w", encoding="utf-8") as h:
    #h.write(json.dumps(mostcom_11_contexts, ensure_ascii=False))
    for key, values in mostcom_11_contexts.items():
        h.write(f'\n {key}: \n')
        for value in values:
            h.write(f'{value} \n')

#for abstract in just_texts:
#    for word in mostcom_11:
#        if word in abstract:
#            context = 



#### Create Wordcloud

text = ' '.join(all_words)

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


#a = just_texts[1]
#b = nlp(a)
#
#for c in b:
#    print(c.lemma_)


#for key,value in all_abstracts.items():
    #print(key, value)
    
