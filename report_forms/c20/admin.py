from django.contrib import admin
from report_forms.c20.models import c20

class c20Admin(admin.ModelAdmin):
    list_display = ('case_id', 'hospital_registration_number', 'date_of_birth', 'diagnosis_code', 'type_of_unit', 'patient_allergic_aspirin', 'aspirin_intolerance', 'type_of_discharge', 'type_of_discharge_empty', 'aspirin_refusal', 'aspirin_at_discharge', 'non_aspirin_platelet', 'date_of_discharge')


admin.site.register(c20, c20Admin)