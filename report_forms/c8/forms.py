from django import forms
from django.forms.models import ModelForm
from report_forms.c8.models import c8
from django.utils.translation import ugettext_lazy as _

class C8Form(ModelForm):
    date_of_birth               = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_admission           = forms.DateTimeField(label=_('Date of hospital admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_discharge           = forms.DateTimeField(label=_('Date of hospital discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_surgical_procedure  = forms.DateTimeField(label=_('Date of first surgical procedure'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))

    def clean(self):
        cleaned_data = super(C8Form, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        date_of_admission = cleaned_data.get("date_of_admission")
        date_of_discharge = cleaned_data.get("date_of_discharge")
        date_of_surgical_procedure = cleaned_data.get("date_of_surgical_procedure")

        if date_of_birth > date_of_admission:
            self._errors["date_of_birth"] = self.error_class([_("Can't be born after admission!")])
            self._errors["date_of_admission"] = self.error_class([_("Can't be born after admission!")])
            del cleaned_data["date_of_birth"]
            del cleaned_data["date_of_admission"]

        if date_of_surgical_procedure < date_of_admission:
            self._errors["date_of_surgical_procedure"] = self.error_class([_("Can't be operated before admission!")])
            self._errors["date_of_admission"] = self.error_class([_("Can't be operated before admission!")])
            del cleaned_data["date_of_surgical_procedure"]
            del cleaned_data["date_of_admission"]

        if date_of_surgical_procedure > date_of_discharge:
            self._errors["date_of_surgical_procedure"] = self.error_class([_("Can't be operated after discharge!")])
            self._errors["date_of_discharge"] = self.error_class([_("Can't be operated after discharge!")])
            del cleaned_data["date_of_surgical_procedure"]
            del cleaned_data["date_of_discharge"]

        return cleaned_data

    class Meta:
        model = c8
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()