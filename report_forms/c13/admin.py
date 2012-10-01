from django.contrib import admin
from report_forms.c13.models import c13

class c13Admin(admin.ModelAdmin):
    list_display = ('job', 'year', 'needlestick_injuries', 'staff_beginning', 'staff_end', 'working_hours_beginning', 'working_hours_end')


admin.site.register(c13, c13Admin)