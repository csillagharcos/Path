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
        dg = cleaned_data.get("diagnosis_group")
        drg = cleaned_data.get("drg")
        icd = cleaned_data.get("icd")
        date_of_admission = cleaned_data.get("date_of_admission")
        date_of_discharge = cleaned_data.get("date_of_discharge")
        date_of_surgical_procedure = cleaned_data.get("date_of_surgical_procedure")

        if (dg == 3 or dg == 4 or dg == 5 or dg == 6 or dg == 7 or dg == 8) and not drg:
            self._errors["drg"] = self.error_class([_("Diagnosis group is not for DRG!")])
            del cleaned_data["drg"]

        if (dg == 0 or dg == 1 or dg == 2 or dg == 5) and not icd:
            self._errors["icd"] = self.error_class([_("Diagnosis group is not for ICD!")])
            del cleaned_data["icd"]

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

class TrendForm(forms.Form):
    date1a = forms.DateTimeField(label=_('First date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date1b = forms.DateTimeField(label=_('First date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date2a = forms.DateTimeField(label=_('Second date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date2b = forms.DateTimeField(label=_('Second date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date3a = forms.DateTimeField(required=False,label=_('Third date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date3b = forms.DateTimeField(required=False,label=_('Third date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))