from django import forms
from django.forms.models import ModelForm
from report_forms.r1.models import r1
from django.utils.translation import ugettext_lazy as _

class r1Form(ModelForm):
    date_of_birth                       = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_admission                   = forms.DateTimeField(label=_('Date of admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FIM_date_of_assess                  = forms.DateTimeField(label=_('FIM date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    BI_date_of_assess                   = forms.DateTimeField(label=_('Barthel index date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SMWT_date_of_assess                 = forms.DateTimeField(label=_('6 minutes walk test date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SF_date_of_assess                   = forms.DateTimeField(label=_('SF-36 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SAT_date_of_assess                  = forms.DateTimeField(label=_('SAT date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FEV_date_of_assess                  = forms.DateTimeField(label=_('FEV-1 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    AI_date_of_assess                   = forms.DateTimeField(label=_('ASIA impairment date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SNC_date_of_assess                  = forms.DateTimeField(label=_('Standard neurological classification of spinal cord injury date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SCI_date_of_assess                  = forms.DateTimeField(label=_('Spinal Cord Independence Measure date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    Other_date_of_assess                = forms.DateTimeField(label=_('Other date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_discharge                   = forms.DateTimeField(label=_('Date of discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FIM_date_of_assess_discharge        = forms.DateTimeField(label=_('FIM date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    BI_date_of_assess_discharge         = forms.DateTimeField(label=_('Barthel index date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SMWT_date_of_assess_discharge       = forms.DateTimeField(label=_('6 minutes walk test date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SF_date_of_assess_discharge         = forms.DateTimeField(label=_('SF-36 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SAT_date_of_assess_discharge        = forms.DateTimeField(label=_('SAT date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FEV_date_of_assess_discharge        = forms.DateTimeField(label=_('FEV-1 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    AI_date_of_assess_discharge         = forms.DateTimeField(label=_('ASIA impairment date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SNC_date_of_assess_discharge        = forms.DateTimeField(label=_('Standard neurological classification of spinal cord injury date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SCI_date_of_assess_discharge        = forms.DateTimeField(label=_('Spinal Cord Independence Measure date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    Other_date_of_assess_discharge      = forms.DateTimeField(label=_('Other date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))







    class Meta:
        model = r1
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()