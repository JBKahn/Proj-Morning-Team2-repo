import random
import re
import requests
from bs4 import BeautifulSoup
 
if __name__ == "__main__":
    wiki_page = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm"
    r = requests.get(wiki_page)
    soup = BeautifulSoup(r.content)
    
    coursesd={}
    for p in soup.findAll('p'):
        s = p.findAll('a', href=True)
        for i in s:
            names = i.contents[0]
            fullLink = i.get('href')
            fixedLink = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/" + fullLink
            sep = requests.get(fixedLink)
            courses = BeautifulSoup(sep.content)

            for code in courses.findAll('a', href=True):
                if code and code.contents and isinstance(code.contents[0], unicode) and code.contents[0].isupper():
                    pass
                    #print code.contents[0]
                   # print re.sub('/^[A-Z]\d{8}$/', '', code.contents[0])
            for section in courses.findAll('font',size=-1):
                if section and isinstance(section.contents[0], unicode):
                    print re.search('[A-Z][0-9][0-9]', section.contents[0], section.contents[0])
            

# [{code: code, section:section,location:location, instructor:instructor...},
#     {code: code, section:section,location:location, instructor:instructor...},
#{code: code, section:section,location:location, instructor:instructor...},
#{code: code, section:section,location:location, instructor:instructor...},
# ]

