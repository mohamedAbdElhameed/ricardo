from django import forms
from django.forms import Form
from likert_field.forms import LikertFormField


class SurveyForm(Form):
    rate = LikertFormField()
    review = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))