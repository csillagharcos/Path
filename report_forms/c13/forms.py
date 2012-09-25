from django import forms
from django.forms.models import ModelForm, ModelChoiceField
from report_forms.c13.models import c13, joblist
from django.utils.translation import ugettext_lazy as _

class englishJoblist(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.job_english

    def __unicode__(self):
        return _('puss')

class hungarianJoblist(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.job_hungarian
    def __unicode__(self):
        return _('puss')



class C13Form(ModelForm):
    job =   englishJoblist(queryset=joblist.objects.all())
    class Meta:
        model = c13
        exclude = ('added_by')

class C13Form_hungarian(ModelForm):
    job =   hungarianJoblist(queryset=joblist.objects.all())
    class Meta:
        model = c13
        exclude = ('added_by')


class FileUploadForm(forms.Form):
    file  = forms.FileField()