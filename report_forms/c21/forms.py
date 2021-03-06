from django import forms
from django.forms.models import ModelForm
from report_forms.c21.models import c21, diagCode, ROUTE_OF_ADMIN_CHOICES, PENICILIN_ALLERGY_CHOICES
from django.utils.translation import ugettext_lazy as _

class C21Form(ModelForm):
    principal_diagnoses_code= forms.ModelChoiceField(label=_('Principal diagnosis code (ICD-10)'), queryset=None)
    penicilin_allergy       = forms.ChoiceField(label=_('In case of allergy to penicillin, scale of severity?'), required=False, widget=forms.RadioSelect, choices=PENICILIN_ALLERGY_CHOICES, initial=3)
    route_of_admin          = forms.ChoiceField(label=_('Route of administration of first dose'), required=False, widget=forms.RadioSelect, choices=ROUTE_OF_ADMIN_CHOICES, initial=1)
    ''' date - time '''
    date_of_wound_close     = forms.DateTimeField(label=_('Date and time of surgical wound closure'), widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    date_of_first_dose      = forms.DateTimeField(label=_('Date and time of first dose'), required=False, widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    surgical_incision       = forms.DateTimeField(label=_('Date and time of surgical incision'), widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    date_of_last_dose       = forms.DateTimeField(label=_('Date and time of last dose'), required=False, widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    date_of_birth           = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    ''' kg '''
    weight_of_patient       = forms.IntegerField(label=_('Weight of patient (kg)'), widget=forms.TextInput(attrs={'class':'size'}))
    ''' mg '''
    first_dose              = forms.FloatField(label=_('First dose of first antibiotic drug'), required=False, widget=forms.TextInput(attrs={'class':'milligramm'}))
    second_dose             = forms.FloatField(label=_('Second dose of first antibiotic drug'), required=False, widget=forms.TextInput(attrs={'class':'milligramm'}))
    total_dose_in_24h       = forms.FloatField(label=_('Total doses in 24 hours'), required=False, widget=forms.TextInput(attrs={'class':'milligramm'}))

    def __init__(self, language_code="hu", *args, **kwargs):
        super(C21Form, self).__init__(*args, **kwargs)
        if diagCode.objects.filter(language=language_code):
            self.fields['principal_diagnoses_code'].queryset = diagCode.objects.filter(language=language_code)
        else:
            self.fields['principal_diagnoses_code'].queryset = diagCode.objects.filter(language="hu")
        self.fields['principal_diagnoses_code'].empty_label = None

    def clean(self):
        cleaned_data = super(C21Form, self).clean()
        surgical_incision = cleaned_data.get("surgical_incision")
        date_of_wound_close = cleaned_data.get("date_of_wound_close")
        date_of_last_dose = cleaned_data.get("date_of_last_dose")
        date_of_first_dose = cleaned_data.get("date_of_first_dose")

        if date_of_first_dose > date_of_last_dose:
            self._errors["date_of_first_dose"] = self.error_class([_("Date of last dose happened before date of first dose!")])
            self._errors["date_of_last_dose"] = self.error_class([_("Date of last dose happened before date of first dose!")])
            del cleaned_data["date_of_first_dose"]
            del cleaned_data["date_of_last_dose"]

        if surgical_incision > date_of_wound_close:
            self._errors["surgical_incision"] = self.error_class([_("Can't close the wound before the incision!")])
            self._errors["date_of_wound_close"] = self.error_class([_("Can't close the wound before the incision!")])
            del cleaned_data["surgical_incision"]
            del cleaned_data["date_of_wound_close"]

        return cleaned_data

    class Meta:
        model = c21
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