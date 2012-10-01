from django.contrib import admin
from report_forms.c8.models import c8

class c8Admin(admin.ModelAdmin):
    list_display = ('patient_id', 'case_id', 'date_of_birth', 'date_of_admission', 'patient_admission_status', 'type_of_admission', 'type_of_admission', 'date_of_surgical_procedure', 'date_of_discharge', 'patient_discharge_status', 'diagnosis_group', 'icd', 'drg')

admin.site.register(c8, c8Admin)