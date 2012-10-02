from django import forms
from django.forms.models import ModelForm
from report_forms.c1.models import c1, c1OtherDiagnose
from django.utils.translation import ugettext_lazy as _

class C1Form(ModelForm):
    other_diagnoses   = forms.MultipleChoiceField(label=_('Other diagnoses'), choices=[(item.pk, item.name) for item in c1OtherDiagnose.objects.all()], widget=forms.CheckboxSelectMultiple())
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_delivery  = forms.DateTimeField(label=_('Date and time of delivery'), widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))

    class Meta:
        model = c1
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()