from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^new/$', 'quits.views.new_group', name='new_group'),
    url(r'^(\d+)/view_group/$', 'quits.views.view_group', name='view_group'),
    url(r'^(\d+)/edit_group/$', 'quits.views.edit_group', name='edit_group'),
    url(r'^(\d+)/delete$', 'quits.views.delete_group', name='delete_group'),
    url(r'^(\d+)/new_payment/$', 'quits.views.new_payment', name='new_payment'),
    url(r'^(\d+)/add_members/$', 'quits.views.add_members', name='add_members'),
    url(r'^(\d+)/payments/(\d+)/edit/$', 'quits.views.edit_payment', name='edit_payment'),
    url(r'^(\d+)/payments/delete$', 'quits.views.delete_payment', name='delete_payment'),
    url(r'^(\d+)/payments/restore$', 'quits.views.restore_payment', name='restore_payment'),
    url(r'^(\d+)/activity_log/$', 'quits.views.activity_log', name='activity_log'),
)
