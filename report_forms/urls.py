from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'c1$', 'report_forms.c1.views.Display', name='c1_display'),
    url(r'c1/import$', 'report_forms.c1.views.Import', name='c1_import'),
    url(r'c1/statistics$', 'report_forms.c1.views.Statistics', name='c1_stat'),
)