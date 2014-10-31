import re
import collections
import random
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse

''' Searches for the expressions below after parsing html codes '''
uoft_timetable_website = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm"
regex_for_strip = re.compile(r'[\n\r\t]')
regex_for_empt = re.compile(r'\xc2\xa0')

def parse_timetable():
     ''' Returns a collection of courses offered by department. '''
     parse_timetable_url = urlparse(uoft_timetable_website)
     table = soupified(uoft_timetable_website, 'li')
     
     for dept in table.findAll(href=True):
          url_dept = dept.get('href')
          if url_dept.endswith('.html'):
               # and not url_dept.startswith('assem'):
               build_full_link = parse_timetable_url.geturl().rsplit('/',1)[0] + '/' + url_dept
               print parse_course_offerings(build_full_link)
               
def parse_course_offerings(course_link):
     ''' Process link that contains information about a list of courses offered by department.
              Returns the course info as dictionaries where key is the course code and values representing course schedule offered. '''
     
     row = 3
     course_offering_and_info = collections.defaultdict(list)
     course_table = soupified(course_link,'table')
     table_rows = course_table.findAll("tr")
     total_rows = len(table_rows)
     
     
     while row < total_rows:
          course_code_out, course_info_out, is_cancelled = get_course_information(table_rows[row])
          
          # skips empty lists
          if not(all([x is '' for x in course_info_out])) and row < total_rows:
               course_code, course_info, is_cancelled = get_course_information(table_rows[row])
               course_offering_and_info[course_code].append(course_info)
               row += 1
     
               if not is_cancelled:
                    course_offering_and_info[course_code].append(course_info)
          row+=1

          while True and row < total_rows:
               potential_course_code, alternative_lecture_info, is_cancelled = get_course_information(table_rows[row])
         
               if not potential_course_code:
                    if not is_cancelled:
                         course_offering_and_info[course_code].append(merge_course_info(course_info, alternative_lecture_info))
                    row += 1
               else:
                    break          
              
     return course_offering_and_info

def merge_course_info(full_course_info, differing_course):
     ''' Merges the rest of altern. schedule time offered per course, that is, if it offers more than one schedule time '''    
     
     course_info = []
    
     for i in range(len(differing_course)):
          if not differing_course[i]:
               if i >= len(full_course_info):
                    course_info.append('')
               else:
                    course_info.append(full_course_info[i])
          else:
               course_info.append(differing_course[i])
     return course_info 

''' Helper functions '''

def cleanText(text):
     ''' Returns a string of course description without the escape seq. characters (i.e \r,\n). '''
     
     regex = re.compile(r'[\n\r\t]')
     stripString = regex.sub('', text).rstrip(",")
     finalString = re.sub(r'\xc2\xa0',"",stripString)
     return finalString    

def soupified(uoft_timetable_website, some_string):
     ''' Accesses data on the website and breaks down its contents '''
     req_content_timetable = requests.get(uoft_timetable_website)
     parse_website_content = BeautifulSoup(req_content_timetable.content)
     table = parse_website_content.find(some_string)   
     
     return table

def get_course_information(tr):
     ''' Returns course code, courses schedule offerings, and status of sched.'''
     course_info = [", ".join(cell.findAll(text=True)) for cell in tr.findAll('td')]
     course_code = cleanText(course_info[0].encode('utf-8'))
     course_info_report = []
     
     for content in [2, 3, 5, 6, 7]:
          if content < len(course_info):
               course_info_report.append(cleanText(course_info[content].encode('utf-8')))
          else:
               course_info_report.append('')
               
     cancelled_schedules = len(course_info) >= 5 and (course_info[4] == 'Cancel')
     
     return course_code, course_info_report, cancelled_schedules
     

if __name__ == "__main__":
     parse_timetable()
