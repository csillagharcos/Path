from django import forms
from django.forms.models import ModelForm
from report_forms.r1.models import r1
from django.utils.translation import ugettext_lazy as _

class r1Form(ModelForm):
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('[click here]')}))

    class Meta:
        model = r1
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()