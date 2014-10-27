import re
import collections
import random
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

''' Searches for the expressions below after parsing html codes '''
regex_for_strip = re.compile(r'[\n\r\t]')
regex_for_empt = re.compile(r'\xc2\xa0')

def cleanText(text):
     ''' Returns a string of course description without the escape seq. characters (i.e \r,\n). '''
     
     regex = re.compile(r'[\n\r\t]')
     stripString = regex.sub('', text).rstrip(",")
     finalString = re.sub(r'\xc2\xa0',"",stripString)
     return finalString


def parseCourseTable(link): 
     ''' Process link that contains information about a list of courses offered by department.
         Returns the course info as dictionaries where key is the course code and values representing course schedule offered. '''

     popular_courses=[]    
     courses_offered = collections.defaultdict(list)     
     sep = requests.get(link)
     course_page = BeautifulSoup(sep.content)
     table = course_page.find('table')
     tableContent=table.findAll('tr')
     html_table_size = len(tableContent) - 1 
     
     
     for sched_row in range(html_table_size):
          course_info = [", ".join(cell.findAll(text=True)) for cell in tableContent[sched_row].findAll('td')]
          other_sched = [", ".join(cell.findAll(text=True)) for cell in tableContent[sched_row+1].findAll('td')]
          main_sched_offered = get_main_sched_time(course_info, courses_offered, sched_row)
          other_schedules = get_other_sched_offered(course_info, other_sched, popular_courses, courses_offered, sched_row)
               
     return courses_offered
          
 
def get_main_sched_time(course_info, courses, index):
     ''' Retrieves the first offered class schedule time for each courses and adds it in the courses collection '''
     
     if (len(course_info) > 7) and not(re.match(r'\xc2\xa0',course_info[0].encode('utf-8'))):
          course_code=cleanText(course_info[0].encode('utf-8'))
          courses[course_code].append([cleanText(course_info[index].encode('utf-8')) for index in [2,3,5,6,7]])  
          
     return courses


def get_other_sched_offered(course_info, other_sched, listCode, courses, index):
     ''' Retrieves the rest of schedule time offered per course, that is, if it offeres more than one schedule time. 
         Adds schedule in the courses collection '''
     
     if re.match(r'\xc2\xa0',other_sched[0].encode('utf-8')):
          if not(re.match(r'\xc2\xa0',course_info[0].encode('utf-8'))):
               listCode.append(course_info[0])
               
     # Handles other schedule courses offered.        
     if (len(course_info) > 7) and re.match(r'\xc2\xa0',course_info[0].encode('utf-8')):
          course_code=cleanText(listCode[-1].encode('utf-8'))
          courses[course_code].append([cleanText(course_info[index].encode('utf-8')) for index in [2,3,5,6,7]])
          
     return courses
     

def parseTimetable():
     ''' Returns a collection of courses offered by department. '''
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
