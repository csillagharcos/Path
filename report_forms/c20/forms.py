from django import forms
from django.forms.models import ModelForm
from report_forms.c20.models import c20
from django.utils.translation import ugettext_lazy as _

class C20Form(ModelForm):
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_discharge = forms.DateTimeField(label=_('Date of discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))

    def clean(self):
        cleaned_data = super(C20Form, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        date_of_discharge = cleaned_data.get("date_of_discharge")
        patient_allergic_aspirin = cleaned_data.get("patient_allergic_aspirin")
        aspirin_intolerance = cleaned_data.get("aspirin_intolerance")
        if date_of_birth > date_of_discharge:
            self._errors["date_of_birth"] = self.error_class([_("Can't born after discharge!")])
            self._errors["date_of_discharge"] = self.error_class([_("Can't born after discharge!")])
            del cleaned_data["date_of_birth"]
            del cleaned_data["date_of_discharge"]

        if patient_allergic_aspirin and not aspirin_intolerance:
            self._errors["aspirin_intolerance"] = self.error_class([_("Aspirin contradiction should be yes, since patient is allergic to aspirin!")])
            del cleaned_data["aspirin_intolerance"]

        return cleaned_data

    class Meta:
        model = c20
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

class AnonymStatForm(forms.Form):
    endDate = forms.DateTimeField(label=_('Date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))