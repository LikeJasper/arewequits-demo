from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'arewequits.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^we-forgot-the-crackers-gromit/', include(admin.site.urls)),
    url(r'^about/$', 'quits.views.about', name='about'),
    url(r'^groups/', include('quits.urls')),
    url(r'^users/', include('quits_users.urls')),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        'quits.views.home_files', name='home_files'),
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^$', 'quits.views.home', name='home'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
