from django import forms
from django.core.exceptions import ValidationError


class ROSIForm(forms.Form):
    student_num = forms.IntegerField()
    password = forms.IntegerField()

    def clean_student_num(self):
        student_num = str(self.cleaned_data['student_num'])
        if len(student_num) != 9:
            raise ValidationError("Student number must be 9 digits.")
        return student_num

    def clean_password(self):
        password = str(self.cleaned_data['password'])
        if len(password) != 6:
            raise ValidationError("password must be 6 digits.")
        return password
