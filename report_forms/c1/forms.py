from django import forms
from django.forms.models import ModelForm
from report_forms.c1.models import c1
from django.utils.translation import ugettext_lazy as _

class C1Form(ModelForm):
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))
    date_of_delivery  = forms.DateTimeField(label=_('Date of delivery'), widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('[click here]')}))
    class Meta:
        model = c1
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()