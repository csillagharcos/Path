from django import forms
from django.forms.models import ModelForm, ModelChoiceField
from report_forms.c13.models import c13, joblist
from django.utils.translation import ugettext_lazy as _

class englishJoblist(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.job_english

class hungarianJoblist(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.job_hungarian

class C13Form(ModelForm):
    job =   englishJoblist(queryset=joblist.objects.all(), label=_('Job'))

    def clean(self):
        cleaned_data = super(C13Form, self).clean()
        staff_beginning = cleaned_data.get("staff_beginning")
        staff_end = cleaned_data.get("staff_end")
        working_hours_beginning = cleaned_data.get("working_hours_beginning")
        working_hours_end = cleaned_data.get("working_hours_end")

        if not staff_beginning:
            self._errors["staff_beginning"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["staff_beginning"]

        if not staff_end:
            self._errors["staff_end"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["staff_end"]

        if not working_hours_beginning:
            self._errors["working_hours_beginning"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["working_hours_beginning"]

        if not working_hours_end:
            self._errors["working_hours_end"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["working_hours_end"]

        return cleaned_data

    class Meta:
        model = c13
        exclude = ('added_by')

class C13Form_hungarian(ModelForm):
    job =   hungarianJoblist(queryset=joblist.objects.all(), label=_('Job'))

    def clean(self):
        cleaned_data = super(C13Form, self).clean()
        staff_beginning = cleaned_data.get("staff_beginning")
        staff_end = cleaned_data.get("staff_end")
        working_hours_beginning = cleaned_data.get("working_hours_beginning")
        working_hours_end = cleaned_data.get("working_hours_end")

        if not staff_beginning:
            self._errors["staff_beginning"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["staff_beginning"]

        if not staff_end:
            self._errors["staff_end"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["staff_end"]

        if not working_hours_beginning:
            self._errors["working_hours_beginning"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["working_hours_beginning"]

        if not working_hours_end:
            self._errors["working_hours_end"] = self.error_class([_("Can't be zero!")])
            del cleaned_data["working_hours_end"]

        return cleaned_data

    class Meta:
        model = c13
        exclude = ('added_by')


class FileUploadForm(forms.Form):
    file  = forms.FileField()

class TrendForm(forms.Form):
    date1a = forms.IntegerField(label=_('First date'), widget=forms.TextInput(attrs={'placeholder':_('(yyyy)')}))
    date2a = forms.IntegerField(label=_('Second date'), widget=forms.TextInput(attrs={'placeholder':_('(yyyy)')}))
    date3a = forms.IntegerField(required=False,label=_('Third date'), widget=forms.TextInput(attrs={'placeholder':_('(yyyy)')}))

class AnonymStatForm(forms.Form):
    endDate = forms.IntegerField(label=_('Date'), widget=forms.TextInput(attrs={'placeholder':_('(yyyy)')}))
