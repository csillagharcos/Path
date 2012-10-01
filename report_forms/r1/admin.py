from django.contrib import admin
from report_forms.r1.models import r1

class r1Admin(admin.ModelAdmin):
    list_display = ('patient_id', 'case_id', 'date_of_birth', 'field_of_rehab', 'field_of_rehab_other', 'date_of_admission', 'FIM_applied', 'FIM_date_of_assess', 'FIM_date_of_assess', 'BI_applied', 'BI_date_of_assess', 'BI_score', 'SMWT_applied', 'SMWT_date_of_assess', 'SMWT_score', 'SF_applied', 'SF_date_of_assess', 'SF_score', 'SAT_applied', 'SAT_date_of_assess', 'SAT_score', 'FEV_applied', 'FEV_date_of_assess', 'FEV_score', 'AI_applied', 'AI_date_of_assess', 'AI_score', 'SNC_applied', 'SNC_date_of_assess', 'SNC_score', 'SCI_applied', 'SCI_date_of_assess', 'SCI_score', 'Other_applied', 'Other_name_of', 'Other_date_of_assess', 'Other_score', 'patient_discharge_status', 'discharge', 'if_unplanned', 'date_of_discharge', 'FIM_applied_discharge','FIM_date_of_assess_discharge', 'FIM_score_discharge', 'BI_applied_discharge', 'BI_date_of_assess_discharge', 'BI_score_discharge', 'SMWT_applied_discharge', 'SMWT_date_of_assess_discharge', 'SMWT_score_discharge', 'SF_applied_discharge', 'SF_date_of_assess_discharge', 'SF_score_discharge', 'SAT_applied_discharge', 'SAT_date_of_assess_discharge', 'SAT_score_discharge', 'FEV_applied_discharge', 'FEV_date_of_assess_discharge', 'FEV_score_discharge', 'AI_applied_discharge', 'AI_date_of_assess_discharge', 'AI_score_discharge', 'SNC_applied_discharge', 'SNC_date_of_assess_discharge', 'SNC_score_discharge', 'SCI_applied_discharge', 'SCI_date_of_assess_discharge', 'SCI_score_discharge', 'Other_applied_discharge', 'Other_name_of_discharge', 'Other_date_of_assess_discharge', 'Other_score_discharge')
admin.site.register(r1, r1Admin)