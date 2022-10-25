from django import forms


class TeamForm(forms.Form):
    name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)


class EmployeeForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    tenure = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
