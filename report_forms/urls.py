from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'report_forms.views.list_report_forms', name="report_forms"),

    url(r'c1$', 'report_forms.c1.views.Display', name='c1_display'),
    url(r'c1/import$', 'report_forms.c1.views.Import', name='c1_import'),
    url(r'c1/statistics$', 'report_forms.c1.views.Statistics', name='c1_stat'),
    url(r'c1/template$', 'report_forms.c1.views.Template', name='c1_template'),

    url(r'c21$', 'report_forms.c21.views.Display', name='c21_display'),
    url(r'c21/import$', 'report_forms.c21.views.Import', name='c21_import'),
    url(r'c21/statistics$', 'report_forms.c21.views.Statistics', name='c21_stat'),
    url(r'c21/template$', 'report_forms.c21.views.Template', name='c21_template'),

    url(r'c23$', 'report_forms.c23.views.Display', name='c23_display'),
    url(r'c23/import$', 'report_forms.c23.views.Import', name='c23_import'),
    url(r'c23/statistics$', 'report_forms.c23.views.Statistics', name='c23_stat'),
    url(r'c23/template$', 'report_forms.c23.views.Template', name='c23_template'),

    url(r'c24$', 'report_forms.c24.views.Display', name='c24_display'),
    url(r'c24/import$', 'report_forms.c24.views.Import', name='c24_import'),
    url(r'c24/statistics$', 'report_forms.c24.views.Statistics', name='c24_stat'),
    url(r'c24/template$', 'report_forms.c24.views.Template', name='c24_template'),

    url(r'c31$', 'report_forms.c31.views.Display', name='c31_display'),
    url(r'c31/import$', 'report_forms.c31.views.Import', name='c31_import'),
    url(r'c31/statistics$', 'report_forms.c31.views.Statistics', name='c31_stat'),
    url(r'c31/template$', 'report_forms.c31.views.Template', name='c31_template'),

    url(r'c32$', 'report_forms.c32.views.Display', name='c32_display'),
    url(r'c32/import$', 'report_forms.c32.views.Import', name='c32_import'),
    url(r'c32/statistics$', 'report_forms.c32.views.Statistics', name='c32_stat'),
    url(r'c32/template$', 'report_forms.c32.views.Template', name='c32_template'),

    url(r'c8$', 'report_forms.c8.views.Display', name='c8_display'),
    url(r'c8/import$', 'report_forms.c8.views.Import', name='c8_import'),
    url(r'c8/statistics$', 'report_forms.c8.views.Statistics', name='c8_stat'),
    url(r'c8/template$', 'report_forms.c8.views.Template', name='c8_template'),

    url(r'c9p$', 'report_forms.c9.views.Display_patient', name='c9_patient_display'),
    url(r'c9o$', 'report_forms.c9.views.Display_operation', name='c9_operation_display'),
    url(r'c9/import$', 'report_forms.c9.views.Import', name='c9_import'),
    url(r'c9/statistics$', 'report_forms.c9.views.Statistics', name='c9_stat'),
    url(r'c9/templateo$', 'report_forms.c9.views.operation_Template', name='c9_operation_template'),
    url(r'c9/templatep$', 'report_forms.c9.views.patients_Template', name='c9_patient_template'),

    url(r'c13$', 'report_forms.c13.views.Display', name='c13_display'),
    url(r'c13/statistics$', 'report_forms.c13.views.Statistics', name='c13_stat'),
    url(r'c13/template$', 'report_forms.c13.views.Template', name='c13_template'),

    url(r'c20$', 'report_forms.c20.views.Display', name='c20_display'),
    url(r'c20/import$', 'report_forms.c20.views.Import', name='c20_import'),
    url(r'c20/statistics$', 'report_forms.c20.views.Statistics', name='c20_stat'),
    url(r'c20/template$', 'report_forms.c20.views.Template', name='c20_template'),

    url(r'r1$', 'report_forms.r1.views.Display', name='r1_display'),
    url(r'r1/import$', 'report_forms.r1.views.Import', name='r1_import'),
    url(r'r1/statistics$', 'report_forms.r1.views.Statistics', name='r1_stat'),
    url(r'r1/template$', 'report_forms.r1.views.Template', name='r1_template'),

)