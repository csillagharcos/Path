from django.forms import ModelForm
from report_forms.c1.models import c1

class C1Form(ModelForm):
    class Meta:
        model = c1
        exclude = ('added_by')

