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
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    #Web
    url(r'^accounts/login/$', login_page),
    url(r'^accounts/logout/$', logout_page),                   
    url(r'^register/$', register_page),
    url(r'^(?P<uid>\w*)/bankaccountregister/$', bank_account_page),
    url(r'^(?P<uid>\w*)/cashregister/$', cash_page),
    url(r'^(?P<uid>\w*)/creditcardregister/$', credit_card_page),
    url(r'^(?P<uid>\w*)/stockaccountregister/$', stock_account_page),
    url(r'^(?P<uid>\w*)/historyregister/$', history_page),                
    url(r'^$', main_page),

    #adminpage
    url(r'^admin/', include(admin.site.urls)),

    #mobile
    url(r'^registration$', register_page_phone),
    url(r'^authenticate/getaccesstoken$', login_page_phone),

    url(r'^(?P<uid>\w*)/bankaccounts/', bank_account),
    url(r'^(?P<uid>\w*)/cashs/', cash),
    url(r'^(?P<uid>\w*)/creditcards/', credit_card),
    url(r'^(?P<uid>\w*)/stockaccounts/', stock_account),
    url(r'^(?P<uid>\w*)/histories/$', histories_request),
    url(r'^(?P<uid>\w*)$', uid_request),
                       
   
    
)
    
