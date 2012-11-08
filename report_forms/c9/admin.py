from django.contrib import admin
from report_forms.c9.models import c9_operation, c9_patient

class c9_oAdmin(admin.ModelAdmin):
    list_display = ('central_operating_unit','operating_unit','type_of_or','weekday_open_time','weekday_close_time','weekday_staffed_days','saturday_open_time','saturday_close_time','saturday_staffed_days','sunday_open_time','sunday_close_time','sunday_staffed_days','hygiene_category','professional_field','preparatory_room','postoperative_room','observation_begins','observation_ends')

class c9_pAdmin(admin.ModelAdmin):
    list_display = ('central_operating_unit','operating_unit','date','type_of_day','case_number','patient_identifier','patient_arrive_time','anesthesia_start','surgery_start','surgery_end','anesthesia_end','patient_leave_time')


admin.site.register(c9_patient, c9_pAdmin)
admin.site.register(c9_operation, c9_oAdmin)
