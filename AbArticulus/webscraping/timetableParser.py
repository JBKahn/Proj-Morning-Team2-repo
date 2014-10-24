import random
import re
import requests
from bs4 import BeautifulSoup

def cleanDescription(string):
     stripString=string.split("\n")
     stripSpace=stripString[0].rstrip(" ")
     return re.sub(r'\xc2\xa0',"",stripSpace).rstrip(",")
 
def parseCourseTable(link):
	''' Returns key, value pairs in the following format: {courseCode:[courseDesc, time, lec...] '''
     dicts={}
     sep = requests.get(link)
     course_page = BeautifulSoup(sep.content)
     table = course_page.find('table')
     for row in table.findAll('tr'):
          cinfo = [", ".join(cell.findAll(text=True)) for cell in row.findAll('td')]
          convert=[cleanDescription(inst.encode('utf-8')) for inst in cinfo]
          
          if len(convert) > 9:
               codeCode=cleanDescription(cinfo[0].encode('utf-8'))
               courseDesc=cleanDescription(cinfo[2].encode('utf-8'))
               lec=cleanDescription(cinfo[3].encode('utf-8'))
               time=cleanDescription(cinfo[5].encode('utf-8'))
               loc=cleanDescription(cinfo[6].encode('utf-8'))
               instructor=cleanDescription(cinfo[7].encode('utf-8'))
               if not dicts.has_key(codeCode):
                    dicts[codeCode]=[courseDesc,lec,time,loc,instructor]
               else:
                    dicts[codeCode].append([courseDesc,time,lec,loc,instructor])
                    
                    
     return dicts

def buildDict(lists):
     pass

def parseCourse(listInfo):
    pass
    
 
if __name__ == "__main__":
     Timetable = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm"
     r = requests.get(Timetable)
     soup = BeautifulSoup(r.content)
    
     coursesInformation={}
     for li in soup.findAll('li'):
          i = li.find('a', href=True)
          names = i.contents[0]
          fullLink = i.get('href')
          if len(fullLink) > 10:
               continue
          fixedLink = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/" + fullLink
          parseCourseTable(fixedLink)

          print parseCourseTable(fixedLink)
