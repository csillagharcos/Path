from django import forms
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from report_forms.c9.models import c9_patient, c9_operation

class C9_patient_Form(ModelForm):
    date                = forms.DateField(label=_('Date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    patient_arrive_time = forms.TimeField(label=_('Time patient arrives to OR'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    anesthesia_start    = forms.TimeField(required= False, label=_('Anesthesia start'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    surgery_start       = forms.TimeField(required= False, label=_('Surgery start'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    surgery_end         = forms.TimeField(required= False, label=_('Surgery end'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    anesthesia_end      = forms.TimeField(required= False, label=_('Anesthesia end'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    patient_leave_time  = forms.TimeField(label=_('Time patient leaves OR'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))

    class Meta:
        model = c9_patient
        exclude = ('added_by')

class C9_operation_Form(ModelForm):
    weekday_open_time    = forms.TimeField(label=_('Normal time of opening on weekdays'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    weekday_close_time   = forms.TimeField(label=_('Normal time of closing on weekdays'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    saturday_open_time   = forms.TimeField(required= False, label=_('Normal time of opening on saturdays'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    saturday_close_time  = forms.TimeField(required= False, label=_('Normal time of closing on saturdays'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    sunday_open_time     = forms.TimeField(required= False, label=_('Normal time of opening on sundays and holidays'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    sunday_close_time    = forms.TimeField(required= False, label=_('Normal time of closing on sundays and holidays'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    observation_begins   = forms.DateField(label=_('Beginning of observational period'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    observation_ends     = forms.DateField(label=_('End of observational period'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))

    class Meta:
        model = c9_operation
        exclude = ('added_by')


class FileUploadForm(forms.Form):
    operation_room  = forms.FileField(required=False)
    patients        = forms.FileField(required=False)

class TrendForm(forms.Form):
    date1a = forms.DateTimeField(label=_('First date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date1b = forms.DateTimeField(label=_('First date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date2a = forms.DateTimeField(label=_('Second date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date2b = forms.DateTimeField(label=_('Second date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date3a = forms.DateTimeField(required=False,label=_('Third date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date3b = forms.DateTimeField(required=False,label=_('Third date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))