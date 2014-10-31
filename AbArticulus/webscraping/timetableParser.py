import re
import collections
import random
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

''' Searches for the expressions below after parsing html codes '''
regex_for_strip = re.compile(r'[\n\r\t]')
regex_for_empt = re.compile(r'\xc2\xa0')

def parse_course_offerings(link): 
     ''' Process link that contains information about a list of courses offered by department.
         Returns the course info as dictionaries where key is the course code and values representing course schedule offered. '''

     sched_row = 0
     popular_courses=[]    
     courses_offered = collections.defaultdict(list)     
     uoft_timetable_site = requests.get(link)
     course_page = BeautifulSoup(uoft_timetable_site.content)
     course_table = course_page.find('table')
     table_content=course_table.findAll('tr')
     html_table_size = len(table_content) - 1 
     
     while sched_row < html_table_size:
          course_info = [", ".join(cell.findAll(text=True)) for cell in table_content[sched_row].findAll('td')]
          other_sched = [", ".join(cell.findAll(text=True)) for cell in table_content[sched_row+1].findAll('td')]
          cancelled = len(course_info) >= 5 and clean_text(course_info[4]) == "Cancel"
          
          if not cancelled:
               main_sched_offered = get_main_sched_time(course_info, courses_offered, sched_row)        
          other_schedules = merge_course_info(course_info, other_sched, popular_courses, courses_offered, sched_row) 
          sched_row+=1
               
     return courses_offered

def parse_timetable():
     ''' Returns a collection of courses offered by department. '''
     
     uoft_timetable_url = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm"
     site_content = requests.get(uoft_timetable_url)
     timetable_and_courses = BeautifulSoup(site_content.content)
    
     for li in timetable_and_courses.findAll('li'):
          department = li.find('a', href=True)
          deparment_links = department.get('href')
          
          if len(deparment_links) > 10:
               continue
          
          courses_and_schedules_url = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/" + deparment_links
          print parse_course_offerings(courses_and_schedules_url)    
          
 
def get_main_sched_time(course_info, courses, index):
     ''' Retrieves the first offered class schedule time for each courses and adds it in the courses collection '''
     
     course_code=clean_text(course_info[0].encode('utf-8'))
     if (len(course_info) > 7 and course_code != 'Course'):
          if not(regex_for_empt.match(course_info[0].encode('utf-8'))):
               first_offered_shed = [clean_text(course_info[index].encode('utf-8')) for index in [2,3,5,6,7]]
               courses[course_code].append(first_offered_shed)
               
     cancelled = len(course_info) >= 5 and clean_text(course_info[4]) == "Cancel"
     
     return courses


def merge_course_info(course_info, other_sched, popular_courses, courses, index):
     ''' Retrieves the rest of schedule time offered per course, that is, if it offeres more than one schedule time. 
         Adds schedule in the courses collection '''
     
     if not(regex_for_empt.match(course_info[0].encode('utf-8'))):
          popular_courses.append(course_info[0])
          
     course_code=clean_text(popular_courses[-1].encode('utf-8'))         
     if (len(course_info) > 7):
          if regex_for_empt.match(course_info[0].encode('utf-8')):
               other_schedule_offered = [clean_text(course_info[index].encode('utf-8')) for index in [2,3,5,6,7]]
               courses[course_code].append(other_schedule_offered)
          
     return courses
     
def clean_text(text):
     ''' Returns a string of course description without the escape seq. characters (i.e \r,\n). '''
     
     strip_string = regex_for_strip.sub('', text).rstrip(",")
     final_string = regex_for_empt.sub("", strip_string)
     return final_string
    

if __name__ == "__main__":

     parse_timetable()
