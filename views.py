# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from cali.models import User, Order, Coupon
import cali.push as push_module
import logging, json, random
import datetime


def add_coupon():
	while True:
		id = random.randint(1000000000000000, 9999999999999999)
		if Coupon.objects.filter(id=id).count() == 0:
			break

	Coupon.objects.create(id=id)
	return id

def coupon(request):
	if not request.user.is_authenticated():
		return redirect(reverse('cms:login') + '?next=' + request.path)
	return render(request, 'cms/coupon.html')

def coupon_issue(request):
	if not request.user.is_authenticated():
		return redirect(reverse('cms:login') + '?next=' + request.path)

	coupon_id_list = [add_coupon() for i in range(int(request.POST['amount']))]

	return render(request, 'cms/coupon_issue.html', {'coupon_id_list': coupon_id_list})

def push(request):
	if not request.user.is_authenticated():
		return redirect(reverse('cms:login') + '?next=' + request.path)
	return render(request, 'cms/push.html', {'user_list': User.objects.order_by('email')})

def push_send(request):
	if not request.user.is_authenticated():
		return redirect(reverse('cms:login') + '?next=' + request.path)

	push_module.push(request.POST.getlist('user_id'), request.POST['title'], request.POST['content'])

	return HttpResponse(u'<script type="text/javascript">alert("사용자들에게 Push 메시지가 발송되었습니다."); location.replace("' + reverse('cms:push') + '");</script>')

def accounts(request):
	if not request.user.is_authenticated():
		return redirect(reverse('cms:login') + '?next=' + request.path)

	return render(request, 'cms/accounts.html')

def accounts_result(request):
	if not request.user.is_authenticated():
		return redirect(reverse('cms:login') + '?next=' + request.path)

	start_date = request.POST['start_date']
	end_date = request.POST['end_date']

	start_date = datetime.datetime.strptime(request.POST['start_date'], "%m/%d/%Y").date()
	end_date = datetime.datetime.strptime(request.POST['end_date'], "%m/%d/%Y").date()
	# end_date += datetime.timedelta(days=1)

	# artist = Artist.objects.all()
	orders = Order.objects.filter(last_updated__gt=start_date, last_updated__lt=end_date+datetime.timedelta(days=1), status=3).exclude(message=request.POST['without'])
	ol = orders.values('last_updated', 'message', 'artist', 'status', 'is_coupon')
	
	ret = dict()
	for order in orders:
		if order.artist not in ret:
			ret[order.artist] = {}
			ret[order.artist]["orders"] = []
			ret[order.artist]["count"] = 0
			ret[order.artist]["coupon"] = 0

		ret[order.artist]["orders"].append(order)
		if order.status == 3:
			if order.is_coupon == False:
				ret[order.artist]["count"] += 1
			else:
				ret[order.artist]["coupon"] += 1

	
	# return HttpResponse('<script type="text/javascript">alert("' + `orders.__class__` + '"); location.replace("' + reverse('cms:accounts') + '");</script>')
	return render(request, 'cms/accounts_result.html', {'start_date': start_date, 'end_date': end_date, 'orders': orders, 'ret': ret})

def pay(request, order_id):
	order = get_object_or_404(Order, id=order_id, status=0)

	return render(request, 'cms/pay.html', {'order': order})

#https://km.paygate.net/display/CS/Verification+after+business+process+completed
#https://km.paygate.net/display/CS/Server-to-Server+transaction+verification
#https://km.paygate.net/pages/viewpage.action?pageId=721172
#https://km.paygate.net/display/CS/Description+of+PGIOForm+Variables

@csrf_exempt
def txn_result(request):
#	ip_addr = request.META['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.META else ''
#	get = json.dumps(request.GET.dict()).decode('unicode_escape')
#	post = json.dumps(request.POST.dict()).decode('unicode_escape')
#	logging.getLogger(__name__).info(u'%-15s GET=%s POST=%s' % (ip_addr, get, post))

	try:
		order = Order.objects.get(id=request.POST['mb_serial_no'])

		if request.POST['unitprice'] == '3000' and request.POST['replycode'] == '0000':
			order.status = 1
			order.save()
	except:
		pass

	return HttpResponse(u'<PGTL><VERIFYRECEIVED>RCVD</VERIFYRECEIVED><TID>' + request.POST['tid'] + u'</TID></PGTL>')
