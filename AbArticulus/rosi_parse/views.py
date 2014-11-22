from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rosi_parse.forms import ROSIForm
from rosi_parse.utils import get_courses_from_rosi

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_variables


class RosiParseAPIView(APIView):
    """
    Accepts ROSI credentials and calls phantom JS and returns the course codes.
    Only accepts post requests.
    """

    @method_decorator(sensitive_variables('password'))
    def post(self, request, format='JSON', *args, **kwargs):
        form = ROSIForm(request.DATA)

        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        studentID = form.cleaned_data["student_num"]
        password = form.cleaned_data["password"]
        return Response(get_courses_from_rosi(studentID, password))
