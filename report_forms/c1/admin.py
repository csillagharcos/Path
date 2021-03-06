from django.contrib import admin
from report_forms.c1.models import c1
from django.utils.translation import ugettext_lazy as _

class c1Admin(admin.ModelAdmin):
    def get_other_diagnoses(self, obj):
        first = True
        namelist = ""
        for diag in obj.other_diagnoses.all():
            if first:
                namelist = diag.name
                first = False
            else:
                namelist = namelist+', '+diag.name
        return namelist
    get_other_diagnoses.short_description = _('Other diagnoses')
    list_display = ('patient_id', 'case_id', 'date_of_birth', 'date_of_delivery', 'number_of_prev_deliveries', 'number_of_prev_deliveries_by_c', 'the_c_section', 'weight_of_the_newborn', 'mother_illness', 'specify_mother_illness', 'drg_code', 'get_other_diagnoses')


admin.site.register(c1, c1Admin)