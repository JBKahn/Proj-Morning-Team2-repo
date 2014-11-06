from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import subprocess
import sys
from rosi_parse.forms import ROSIForm


class RosiParseAPIView(APIView):
    """
    Accepts ROSI credentials and calls phantom JS and returns the course codes.
    Only accepts post requests.
    """
       

    def post(self, request, format='JSON', *args, **kwargs):
        form = ROSIForm(request.POST)

        if not form.is_valid():
            return Response(form.erors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: invoke your script here tp get the course codes.
        studentID = form.clean_student_num
        password = form.clean_password
        print >> sys.stderr,  "hihhihiih %s" %studentID 
        #Run casperjs along with the parameters
        raw = subprocess.check_output(['./casperjs schedule_parser.js ' + studentID + ' ' + password])
        print "%s" %raw
        course_codes = []
        return Response({"course_codes": course_codes})
