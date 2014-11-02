from django import forms


class ROSIForm(forms.Form):
	student_num = forms.IntegerField()
