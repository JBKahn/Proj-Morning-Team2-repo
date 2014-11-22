from subprocess import check_output, CalledProcessError

from django.views.decorators.debug import sensitive_variables


@sensitive_variables('username', 'password')
def get_courses_from_rosi(username, password):
    try:
        raw_courses = check_output(['./rosi_parse/casperjs', './rosi_parse/schedule_parser.js', username, password])
    except CalledProcessError:
        raise Exception('You must login to your account once before we can, there is a capcha. Or your credentials are bad.')
    return raw_courses.split(',')
