from django import forms
from django.forms.models import ModelForm
from report_forms.c13.models import c13, joblist


class C13Form(ModelForm):
    job =   forms.ChoiceField(choices=[(item.pk, item.english()) for item in joblist.objects.all()])
    class Meta:
        model = c13
        exclude = ('added_by')

class C13Form_hungarian(ModelForm):
    job =   forms.ChoiceField(choices=[(item.pk, item.hungarian()) for item in joblist.objects.all()])
    class Meta:
        model = c13
        exclude = ('added_by')


class FileUploadForm(forms.Form):
    file  = forms.FileField()