from django import forms

from apps.models import Application, ApplicationType


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


class EmployeeCreateForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    fullname = forms.CharField(max_length=50)
    pk = forms.IntegerField()


class EmployeeForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


class VideoModelForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationTypeForm(forms.ModelForm):
    class Meta:
        model = ApplicationType
        fields = '__all__'
