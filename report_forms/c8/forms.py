from django import forms
from django.forms.models import ModelForm
from report_forms.c8.models import c8
from django.utils.translation import ugettext_lazy as _

class C8Form(ModelForm):
    date_of_birth               = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    date_of_admission           = forms.DateTimeField(label=_('Date of hospital admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    date_of_discharge           = forms.DateTimeField(label=_('Date of hospital discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    date_of_surgical_procedure  = forms.DateTimeField(label=_('Date of first surgical procedure'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    class Meta:
        model = c8
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()