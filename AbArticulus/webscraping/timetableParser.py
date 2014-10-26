import re
import collections
import random
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString



def cleanText(text):
     ''' Returns a string of course description without the escape seq. characters (i.e \r,\n). '''
     
     regex = re.compile(r'[\n\r\t]')
     stripString = regex.sub('', text).rstrip(",")
     finalString = re.sub(r'\xc2\xa0',"",stripString)
     return finalString


def parseCourseTable(link): 
     ''' Docstrings here '''

     # index 0: course code
     # index 2: course description
     # index 3: lecture code
     # index 5: times
     # index 6: location
     # index 7: instructor  
     
     listCode=[]    
     courses = collections.defaultdict(list)     
     sep = requests.get(link)
     course_page = BeautifulSoup(sep.content)
     table = course_page.find('table')
     finder=table.findAll('tr')
     
     for row in range(len(finder)-1):          
          course_info = [", ".join(cell.findAll(text=True)) for cell in finder[row].findAll('td')]
          otherSched = [", ".join(cell.findAll(text=True)) for cell in finder[row+1].findAll('td')]
          
          # Handles the first course schedule offered.
          if (len(course_info) > 2 and len(course_info) > 7) and not(re.match(r'\xc2\xa0',course_info[0].encode('utf-8'))):
           
               course_code=cleanText(course_info[0].encode('utf-8'))
               courses[course_code].append([cleanText(course_info[index].encode('utf-8')) for index in [2,3,5,6,7]])
            
          # Retrieves the courses with more than one schedule time
          if re.match(r'\xc2\xa0',otherSched[0].encode('utf-8')):
               if not(re.match(r'\xc2\xa0',course_info[0].encode('utf-8'))):
                    listCode.append(course_info[0])
                     
          # Handles other schedule courses offered.        
          if (len(course_info) > 2 and len(course_info) > 7) and re.match(r'\xc2\xa0',course_info[0].encode('utf-8')):
               course_code=cleanText(listCode[-1].encode('utf-8'))
               courses[course_code].append([cleanText(course_info[index].encode('utf-8')) for index in [2,3,5,6,7]])
        

     return courses
            

def parseTimetable():
     Timetable = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm"
     requestTT = requests.get(Timetable)
     soup = BeautifulSoup(requestTT.content)
    
     for li in soup.findAll('li'):
          department = li.find('a', href=True)
          getContents = department.contents[0]
          fullLink = department.get('href')
          
          if len(fullLink) > 10:
               continue
          
          fixedLink = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/" + fullLink
          print parseCourseTable(fixedLink)     
     
    

if __name__ == "__main__":

     parseTimetable()
