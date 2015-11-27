from django.conf.urls import patterns, include, url, handler404
from quits_users import views
from allauth.account import views as aa_views
from allauth.socialaccount import views as sa_views

urlpatterns = patterns('',
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^new/$', views.signup, name='account_signup'),

    # django-allauth
    url(r'^confirm-email/$', aa_views.email_verification_sent,
        name='account_email_verification_sent'),
    url(r'^confirm-email/(?P<key>\w+)/$', aa_views.confirm_email,
        name='account_confirm_email'),
    url(r'^login/$', aa_views.login, name='account_login'),
    url(r'^logout$', aa_views.logout, name='account_logout'),
    url(r'^password/reset/$', aa_views.password_reset,
        name='account_reset_password'),
    url(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        aa_views.password_reset_from_key,
        name='account_reset_password_from_key'),
    url(r'^password/reset/done/$', aa_views.password_reset_done,
        name='account_reset_password_done'),
    url(r'^password/reset/key/done/$', aa_views.password_reset_from_key_done,
        name='account_reset_password_from_key_done'),
    url(r'^facebook/login/token/$',
        'allauth.socialaccount.providers.facebook.views.login_by_token',
        name='facebook_login_by_token'),
    url(r'^login/error/$', sa_views.login_error, name='socialaccount_login_error'),
    url(r'^login/cancelled/$', sa_views.login_error, name='socialaccount_login_cancelled'),

    # Referenced by django-allauth but not needed
    url(r'^facebook/login/$', handler404, name='facebook_login'),
    url(r'^social_signup/$', handler404, name='socialaccount_signup'),
)
