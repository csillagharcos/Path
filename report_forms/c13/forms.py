from django import forms
from django.forms.models import ModelForm
from report_forms.c13.models import c13

class C13Form(ModelForm):
    class Meta:
        model = c13
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()