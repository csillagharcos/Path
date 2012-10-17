from django.contrib import admin
from report_forms.c23.models import c23

class c23Admin(admin.ModelAdmin):
    list_display = ('case_id', 'hospital_registration_number', 'date_of_birth', 'weight_of_patient', 'principal_diagnoses_code', 'principal_procedure_code', 'procedure_planned', 'patient_allergy', 'generic_name_of_drug', 'penicilin_allergy', 'preoperative_infection', 'type_of_infection', 'surgical_incision', 'antibiotic_given', 'name_of_first_dose', 'first_dose', 'name_of_second_dose', 'second_dose', 'route_of_admin', 'date_of_first_dose', 'total_dose_in_24h', 'date_of_last_dose', 'date_of_wound_close')

admin.site.register(c23, c23Admin)