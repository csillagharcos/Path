from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'report_forms.views.list_report_forms', name="report_forms"),

    url(r'c1$', 'report_forms.c1.views.Display', name='c1_display'),
    url(r'c1/import$', 'report_forms.c1.views.Import', name='c1_import'),
    url(r'c1/statistics$', 'report_forms.c1.views.Statistics', name='c1_stat'),

    url(r'c21$', 'report_forms.c21.views.Display', name='c21_display'),
    url(r'c21/import$', 'report_forms.c21.views.Import', name='c21_import'),
    url(r'c21/statistics$', 'report_forms.c21.views.Statistics', name='c21_stat'),

    url(r'c23$', 'report_forms.c23.views.Display', name='c23_display'),
    url(r'c23/import$', 'report_forms.c23.views.Import', name='c23_import'),
    url(r'c23/statistics$', 'report_forms.c23.views.Statistics', name='c23_stat'),

    url(r'c24$', 'report_forms.c24.views.Display', name='c24_display'),
    url(r'c24/import$', 'report_forms.c24.views.Import', name='c24_import'),
    url(r'c24/statistics$', 'report_forms.c24.views.Statistics', name='c24_stat'),

    url(r'c31$', 'report_forms.c31.views.Display', name='c31_display'),
    url(r'c31/import$', 'report_forms.c31.views.Import', name='c31_import'),
    url(r'c31/statistics$', 'report_forms.c31.views.Statistics', name='c31_stat'),

    url(r'c32$', 'report_forms.c32.views.Display', name='c32_display'),
    url(r'c32/import$', 'report_forms.c32.views.Import', name='c32_import'),
    url(r'c32/statistics$', 'report_forms.c32.views.Statistics', name='c32_stat'),

    url(r'c8$', 'report_forms.c8.views.Display', name='c8_display'),
    url(r'c8/import$', 'report_forms.c8.views.Import', name='c8_import'),
    url(r'c8/statistics$', 'report_forms.c8.views.Statistics', name='c8_stat'),
)