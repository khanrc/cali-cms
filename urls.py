from django.conf.urls import patterns, url

from cms import views

urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
	url(r'^coupon/$|^$', views.coupon, name='coupon'),
	url(r'^coupon/issue$', views.coupon_issue, name='coupon_issue'),
	url(r'^push/$', views.push, name='push'),
	url(r'^push/send$', views.push_send, name='push_send'),
	url(r'^accounts/$', views.accounts, name='accounts'),
	url(r'^accounts/result$', views.accounts_result, name='accounts_result'),
	url(r'^pay/(?P<order_id>\d+)$', views.pay, name='pay'),
	url(r'^txn_result/$', views.txn_result, name='txn_result'),
)

