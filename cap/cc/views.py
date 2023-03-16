 # https://www.youtube.com/watch?v=BppyfPye8eo
import csv, io, ast, time, datetime, django_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
from cc.models import CCm
from ro.models import RO
from cc.forms import CC_Form, CC_Update_Form
# from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import connection
from django.contrib.auth.models import User, Group
# from mail.views import send_email

def home( request ):
	# print( f'{ datetime.datetime.now() } { request.user.username }' )
	print( f'{ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user }' )
	# print( request.__dict__ )
	# print('New Log in')
	# if request.user.username == 'ghost':
	# 	send_email( 'BEAR CAP Log In', 'Ghost has entered the CAP' )

	return render( request, 'cc/welcome.html', {} )


# def view2( request ):
# 	print( f'{ datetime.datetime.now() } { request.user }' )
# 	return HttpResponse( 'Cool Dude')


def view( request ):
	print( f'{ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user } - View Credit Card Transactions' )
	link, all = select_link( request )

	from .filters import CC_Filter
	filter = CC_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	cost = 0
	for i in filter.qs:
		cost	+= i.amount

	context =	{
					'link': link,
					'transactions': filter,
					'count':	n,
					'total_cost': round( cost, 2)
				}
	return render( request, 'cc/view.html', context )


def link( request ):
	d = get_get( request )
	print( d )
	log_id	= request.GET['logid']	# log_id is used by Filter
	payee	= request.GET['payee']

	if 'auto' in d.keys():
		link = ['', 'selected', '']
		all = CCm.objects.filter( log_id=0, payee__contains=payee ).order_by('-posted_date')

	else:
		link, all = select_link( request )

	from .filters import CC_Filter
	filter = CC_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	# print( f'n = {n}' )
	cost = 0
	for i in filter.qs:
		cost	+= i.amount

	context =	{
					'link': link,
					'transactions': filter,
					'count':	n,
					'log_id':	log_id,
					'total_cost': round( cost, 2)
				}
	return render( request, 'cc/link.html', context )


def select_link( request ):
	# Called from view, link
	print( get_get( request ) )

	link = ['', 'selected', '']					#	Drop down default value
	all = CCm.objects.filter( log_id=0 ).order_by('-posted_date')
	key = 'link'
	if key in request.GET:
		status = request.GET[key]
		if status == 'all':
			link = ['selected', '', '']
			all = CCm.objects.all().order_by('-posted_date')

		elif status == 'False':
			link = ['', 'selected', '']
			all = CCm.objects.filter( log_id=0 ).order_by('-posted_date')

		else:
			# print( f'key { key } is not in GET request.')
			link = ['', '', 'selected']
			all = CCm.objects.filter().exclude( log_id=0 ).order_by('-posted_date')

	return link, all


def get_post(request):
	d = {}
	for key in request.POST:
		value = request.POST[key]
		# s += key + ':' + value + '<br>'
		d[key] = value

	return d


def get_get(request):
	print( request.method )
	keys = list( request.GET.keys() )
	print( keys )

	d = {}
	for key in request.GET:
		value = request.GET[key]
		# s += key + ':' + value + '<br>'
		d[key] = value

	return d
