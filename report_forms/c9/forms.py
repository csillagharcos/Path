from django import forms
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from report_forms.c9.models import c9_patient, c9_operation

class C9_patient_Form(ModelForm):
    date                = forms.DateTimeField(label=_('Date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    patient_arrive_time = forms.TimeField(label=_('Time patient arrives to OR'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    patient_leave_time  = forms.TimeField(label=_('Time patient leaves OR'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))

    class Meta:
        model = c9_patient
        exclude = ('added_by')

class C9_operation_Form(ModelForm):
    weekday_open_time   = forms.TimeField(label=_('Weekday normal time of opening'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    weekday_close_time   = forms.TimeField(label=_('Weekday normal time of closing'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    saturday_open_time   = forms.TimeField(label=_('Saturday normal time of opening'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    saturday_close_time   = forms.TimeField(label=_('Saturday normal time of closing'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    sunday_open_time   = forms.TimeField(label=_('Sunday/Holiday normal time of opening'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))
    sunday_close_time   = forms.TimeField(label=_('Sunday/Holiday normal time of closing'), widget=forms.TextInput(attrs={'class':'timepicker', 'placeholder':_('(hh:mm)')}))

    class Meta:
        model = c9_operation
        exclude = ('added_by')


class FileUploadForm(forms.Form):
    operation_room  = forms.FileField()
    patients        = forms.FileField()