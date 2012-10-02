from django import forms
from django.forms.models import ModelForm
from report_forms.c31.models import c31
from django.utils.translation import ugettext_lazy as _

class C31Form(ModelForm):
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_admission = forms.DateTimeField(label=_('Date of hospital admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_discharge = forms.DateTimeField(label=_('Date of hospital discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    class Meta:
        model = c31
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()