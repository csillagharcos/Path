from django import forms
from django.forms.models import ModelForm
from report_forms.c1.models import c1, c1OtherDiagnose
from django.utils.translation import ugettext_lazy as _

class C1Form(ModelForm):
    other_diagnoses   = forms.MultipleChoiceField(label=_('Other diagnoses'), choices=[(item.pk, item.name) for item in c1OtherDiagnose.objects.all()], widget=forms.CheckboxSelectMultiple())
    date_of_birth     = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_delivery  = forms.DateTimeField(label=_('Date and time of delivery'), widget=forms.TextInput(attrs={'class':'datetimepicker', 'placeholder':_('(yyyy-mm-dd hh:mm)')}))

    def clean(self):
        cleaned_data = super(C1Form, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        date_of_delivery = cleaned_data.get("date_of_delivery")
        if date_of_birth > date_of_delivery:
            self._errors["date_of_birth"] = self.error_class([_("Born after date of delivery!")])
            self._errors["date_of_delivery"] = self.error_class([_("Born after date of delivery!")])
            del cleaned_data["date_of_birth"]
        return cleaned_data

    class Meta:
        model = c1
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