from django import forms
from django.forms.models import ModelForm
from report_forms.c32.models import c32
from django.utils.translation import ugettext_lazy as _

class C32Form(ModelForm):
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    date_of_admission = forms.DateTimeField(label=_('Date of hospital admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    date_of_discharge = forms.DateTimeField(label=_('Date of hospital discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    class Meta:
        model = c32
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()