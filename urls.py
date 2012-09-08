from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'Path.views.home', name='home'),
    #url(r'^Path/', include('Path.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reportforms/', include('report_forms.urls')),
)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^translate/', include('rosetta.urls')),
    )