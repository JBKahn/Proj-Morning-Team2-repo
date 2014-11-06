from subprocess import check_output


def get_courses_from_rosi(username, password):
    raw_courses = check_output(['./casperjs schedule_parser.js {} {}'.format(username, password)])
    courses = []
    for course in raw_courses.split(','):
        courses.append({
            'course_code': course.split('-')[0],
            'lecture_section': course.split('-')[1]
        })
    return courses
