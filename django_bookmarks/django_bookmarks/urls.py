from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout


# Uncomment the next two lines to enable the admin:
from django.conf.urls.defaults import *
from bookmarks.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_bookmarks.views.home', name='home'),
    # url(r'^django_bookmarks/', include('django_bookmarks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url('^bookmarks/$', hello),
    url('^time/$', current_datetime),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/login/$', login_page),
    url(r'^accounts/loginPhone/$', login_page_phone),
    url(r'^accounts/logout/$', logout_page),
    url(r'^register/$', register_page),
    url(r'^registerPhone/$', register_page_phone),                       
    url('^test1/$', template_test),
    url(r'^$', main_page),

    #adminpage
    url(r'^admin/', include(admin.site.urls)),
)
