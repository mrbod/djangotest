from django import forms

class NewRepo(forms.Form):
    name = forms.CharField(label='Name', max_length=100)

