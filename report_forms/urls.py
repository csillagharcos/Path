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

)