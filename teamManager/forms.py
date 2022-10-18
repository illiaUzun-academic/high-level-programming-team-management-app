from django import forms


class TeamForm(forms.Form):
    name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
