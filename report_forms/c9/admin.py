from django.contrib import admin
from report_forms.c9.models import c9_operation, c9_patient
from django.utils.translation import ugettext_lazy as _

#class c9Admin(admin.ModelAdmin):
#    list_display = ('patient_id', 'case_id', 'date_of_birth', 'date_of_delivery', 'number_of_prev_deliveries', 'number_of_prev_deliveries_by_c', 'the_c_section', 'weight_of_the_newborn', 'mother_illness', 'specify_mother_illness', 'drg_code', 'get_other_diagnoses')


admin.site.register(c9_patient)
admin.site.register(c9_operation)
