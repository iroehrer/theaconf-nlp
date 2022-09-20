from bs4 import BeautifulSoup
import os
import json
from langdetect import detect

#initialise text for lists
text_list = []
all_abstracts = {}
 
directory = "abstracts/"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    with open(f) as f:
        #reading file contents into the string "html"
        html = f.read() #.decode("utf-8", "ignore")
        
        temp_list = []
        
        #using beautiful soup to parse the document
        soup = BeautifulSoup(html, "html.parser")
        
        raw_text_list = soup.find_all("div", {"data-module": "text"})
        
        #get pure text from html into text_list
        for text in raw_text_list:
            text = text.get_text()
            text_list.append(text.strip())
            temp_list.append(text.strip())
            
        title = temp_list[1]
        print(title)
        #a = detect(title)
        #print(a)
            
        all_abstracts[title] = temp_list
            
        
        pass
            #print(text)
            
        #print(text_list)
        

        #print(all_abstracts)

#print(json.dumps(all_abstracts, sort_keys=True, indent=4))

#for key,value in all_abstracts.items():
    #print(key, value)
    
