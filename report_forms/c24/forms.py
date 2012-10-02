from django import forms
from django.forms.models import ModelForm
from report_forms.c24.models import c24
from report_forms.choices import ROUTE_OF_ADMIN_CHOICES_FOUR, PENICILIN_ALLERGY_CHOICES
from django.utils.translation import ugettext_lazy as _

class C24Form(ModelForm):
    penicilin_allergy       = forms.ChoiceField(label=_('In case of allergy to penicillin, scale of severity?'), required=False, widget=forms.RadioSelect, choices=PENICILIN_ALLERGY_CHOICES, initial=3)
    route_of_admin          = forms.ChoiceField(label=_('Route of administration of first dose'), required=False, widget=forms.RadioSelect, choices=ROUTE_OF_ADMIN_CHOICES_FOUR, initial=1)
    ''' date - time '''
    date_of_wound_close     = forms.DateTimeField(label=_('Date of surgical wound closure'), widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    date_of_first_dose      = forms.DateTimeField(label=_('Date of first dose'), required=False, widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    surgical_incision       = forms.DateTimeField(label=_('Date of surgical incision'), widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    date_of_last_dose       = forms.DateTimeField(label=_('Date of last dose'), required=False, widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))
    date_of_birth           = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    ''' kg '''
    weight_of_patient       = forms.IntegerField(label=_('Weight of patient (kg)'), widget=forms.TextInput(attrs={'class':'size'}))
    ''' mg '''
    first_dose              = forms.FloatField(label=_('First dose'), required=False, widget=forms.TextInput(attrs={'class':'milligramm'}))
    second_dose             = forms.FloatField(label=_('Second dose'), required=False, widget=forms.TextInput(attrs={'class':'milligramm'}))
    other_dose              = forms.FloatField(label=_('Other dose'), required=False, widget=forms.TextInput(attrs={'class':'milligramm'}))
    total_dose_in_24h       = forms.FloatField(label=_('Total doses in 24 hours'), required=False, widget=forms.TextInput(attrs={'class':'milligramm'}))


    class Meta:
        model = c24
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()