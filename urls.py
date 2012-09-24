from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reportforms/', include('report_forms.urls'), name="report_forms"),
    url(r'^knowledgecenter', 'pathstatic.views.knowledge_center', name="knowledge_center"),
    url(r'^$', 'pathstatic.views.homepage', name="homepage"),
    url(r'^login/', 'pathstatic.views.login_page'),
    url(r'^logout', 'pathstatic.views.user_logout'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^translate/', include('rosetta.urls')),
    )