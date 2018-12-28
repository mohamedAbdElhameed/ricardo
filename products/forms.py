from django import forms

class ReviewForm(forms.Form):
    rate = forms.IntegerField(widget=forms.fieldset)