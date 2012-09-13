from django.forms import ModelForm, forms
from report_forms.c21.models import c21

class C21Form(ModelForm):
    class Meta:
        model = c21
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()