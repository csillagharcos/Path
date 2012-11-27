from django import forms
from django.forms.models import ModelForm
from report_forms.c32.models import c32
from django.utils.translation import ugettext_lazy as _

class C32Form(ModelForm):
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_admission = forms.DateTimeField(label=_('Date of hospital admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_discharge = forms.DateTimeField(label=_('Date of hospital discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))

    def clean(self):
        cleaned_data = super(C32Form, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        date_of_admission = cleaned_data.get("date_of_admission")
        date_of_discharge = cleaned_data.get("date_of_discharge")

        if date_of_birth > date_of_admission:
            self._errors["date_of_birth"] = self.error_class([_("Can't be born after admission!")])
            self._errors["date_of_admission"] = self.error_class([_("Can't be born after admission!")])
            del cleaned_data["date_of_birth"]
            del cleaned_data["date_of_admission"]

        if date_of_discharge < date_of_admission:
            self._errors["date_of_admission"] = self.error_class([_("Can't be discharged before admission!")])
            self._errors["date_of_discharge"] = self.error_class([_("Can't be discharged before admission!")])
            del cleaned_data["date_of_admission"]
            del cleaned_data["date_of_discharge"]

        return cleaned_data

    class Meta:
        model = c32
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