from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
        course_codes = []
        return Response({"course_codes": course_codes})
