from django.contrib import admin
from report_forms.c31.models import c31

class c31Admin(admin.ModelAdmin):
    list_display = ('patient_id', 'case_id', 'date_of_birth', 'date_of_admission', 'patient_admission_status', 'date_of_discharge', 'patient_discharge_status', 'icd')

admin.site.register(c31, c31Admin)