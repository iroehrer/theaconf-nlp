from bs4 import BeautifulSoup


#initialise text for lists
text_list = []

#opening the html file
with open("matters-of-urgency.de/" + "analyzing-activist-bodies.html", "r") as f:
    
    #reading file contents into the string "html"
    html = f.read()
    
    #using beautiful soup to parse the document
    soup = BeautifulSoup(html, "html.parser")
    
    #debug: print the html to the console
    #print(soup.prettify())
    
    
    #for child in soup.recursiveChildGenerator():
    #    if child.name:
    #        print(child.name)
            
    #print(soup.get_text())
    
    #find all text areas from html file
    raw_text_list = soup.find_all("div", {"data-module": "text"})
    
    #get pure text from html into text_list
    for text in raw_text_list:
        text = text.get_text()
        text_list.append(text.strip())
        
        print(text)
        
    print(text_list)