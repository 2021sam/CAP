# https://www.youtube.com/watch?v=BppyfPye8eo
import csv, io, ast, time, datetime, django_filters
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Log
from cclog.forms import CC_New_Log_Form, CC_Log_Form, CC_Log_Form2, CC_Log_Form3
from django.contrib.auth.decorators import permission_required
from django.db import connection
# from django.conf.urls import url
from cclog.filters import CC_Log_Filter
from django.contrib.auth.models import User
from mail.views import send_email_attach, get_logs_attach
from cc.models import CCm
from po.models import PO
from vendor.models import VendorModel

vip	= ['sam', 'keith']

#	CC Log - Create a Log
@login_required(login_url='login')	#	login → url name
def log( request ):
	# print( request.method )
	vendors = get_vendors()
	# vendors = VendorModel.objects.filter( inactive = False ).order_by('name')

	if request.method == 'GET':
		print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user.username } Creating a New Log' )
		d = datetime.today().strftime('%Y-%m-%d')
		ghost = ''
		if request.user.username == 'ghost':
			ghost = 'disabled'
			# ghost_title = 'You are a ghost'
			# ghost = 'disabled title="You are a ghost."'

		form = CC_New_Log_Form(initial={'transaction_date': d })
		template = 'cclog/log.html'
		context = { 'form': form, 'vendors': vendors, 'ghost': ghost }
		return render( request, template, context )

	if request.method == "POST":
		# print('post new log')
		form = CC_New_Log_Form( request.POST )
		if form.is_valid():
			# print('save new log')
			i			= form.save()
			i.log_id	= i.id
			i.user_id	= str( request.user )
			i.start		= int( time.time() )

			if VendorModel.objects.filter(pk=i.vendor_id).exists():
				vid = VendorModel.objects.get( pk=i.vendor_id )
				i.vendor_id_key = vid
				# print( 'saved vid')

			i.save()

			attachment = get_logs_attach()
			send_email_attach( 'BEAR CC Log - Attached', 'Log file is attached.', attachment )

			form = CC_Log_Form( instance=i )
			form = disable( form )
			template = 'cclog/view.html'
			context = { 'title': 'New Log Saved',
						'form': form,
						'card': 'x' }
			print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user } - Saved New Log → { i }' )
			return render( request, template, context )

		else:
			print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user } Form Not Valid' )
			print(form.errors)
			return HttpResponse( 'Form is not valid.' )


def get_vendors():
	return VendorModel.objects.filter( inactive = False ).order_by('name')


def remove_keys( vendors, keys ):
	for i in keys:
		del vendors[ i ]

	return vendors


def logs( request ):
	print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user } - View Logs' )
	# ro_list = RO.objects.all()
	# all = Log.objects.all()		# This needs to be in parenthesis
	print(request.user.username)
	print( request.GET )
	if len(request.GET) == 0:
		#	Auto filter to reduce routine requests
		# all = Log.objects.filter(user_id=request.user.username, closed=False).order_by('-log_id')		# 2023.03.05
		#	Only need to filter by closed because it is a reason for them to close !
		#	Despite slow responses.
		all = Log.objects.filter(closed=False).order_by('-log_id')		# 2023.03.05

	if len(request.GET) > 0:
		all = Log.objects.all().order_by( '-log_id' )			# 07/13/2021
		# User.objects.all().order_by('date_joined', '-last_login')
	filter = CC_Log_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	# cost = 0
	# price = 0
	# for i in filter.qs:
	# 	cost	+= i.cost
	# 	price	+= i.price
	# tot = filter.qs.objects.annotate(cost=Sum('cost'))

	context = 	{ 'transactions': filter,
					'count':	n,
					# 'total_cost': round( cost, 2),
					# 'total_price': round( price, 2)
				}
	return render( request, 'cclog/logs.html', context )


def logs2( request ):
	print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user.username } View Linked Logs' )
	# ro_list = RO.objects.all()
	all = Log.objects.all()		# This needs to be in parenthesis

	filter = CC_Log_Filter( request.GET, queryset=all )
	# CC = CCm.objects.all()
	n = len( filter.qs )
	template = 'cclog/logs2.html'
	# template = 'cclog/logs-sam.html'
	# vip = ['sam', 'ghost', 'lynnette']

	context = 	{ 'transactions': filter,
					'count':	n
					# 'vip': vip
					# 'total_cost': round( cost, 2),
					# 'total_price': round( price, 2)
				}
	return render( request, template, context )


#	Does not check for changes
def link_key( i ):
	i.po.clear()
	i.po_cost  = 0
	i.po_price = 0
	i.save()

	qs		= PO.objects.filter( ro=i.ro1, invoice=i.invoice )
	if qs.exists():
		cost = 0
		price = 0
		for j in qs:
			i.po.add( j )
			cost  += j.cost
			price += j.price
			i.po_cost  = round( cost, 2)
			i.po_price = round( price, 2)
			i.save()

	return i



@login_required(login_url='login')	#	login → url name
def update( request ):
	pk = request.POST['choice']
	print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user } Updating Log { pk }' )
	qs = Log.objects.filter(pk=pk)
	if not qs.exists():
		return HttpResponse(f'Log { pk } does not exist.  Call or text 925.575.7070.')

	#	Can not use qs from filter → need to use .get
	i = Log.objects.get( pk=pk )	# Causes matching query does not exist

	#	Current Non Linking Rogue Form
	form = CC_Log_Form( instance = i )

	#	Linking Form
	# if User.objects.filter( username=request.user.username, groups__name='Link').exists():
	if request.user.is_superuser or request.user.username in vip:
		form = CC_Log_Form2( instance = i )

	form.fields['log_id'].widget.attrs['readonly'] = True
	form.fields['user_id'].widget.attrs['readonly'] = True

	title			= 'Update Log'
	template		= 'cclog/update.html'

	if i.voided:
		title		= 'Log Voided'
		template	= 'cclog/view.html'
		form		= disable( form )

	if i.closed:
		title		= 'Log Closed'
		if not request.user.username in vip:
			template	= 'cclog/view.html'
			form		= disable( form )

	# if not request.user.is_superuser and not request.user.username == 'sam':
	if not request.user.is_superuser:
		if not request.user.username in vip:
			if i.user_id != request.user.username:
				title		= 'Non Purchaser View'
				template	= 'cclog/view.html'
				form		= disable( form )

	vendors = get_vendors()

	context = {
				'title': title,
				'i': i,
				'form': form,
				'vendors': vendors
				}
	return render( request, template, context )


# cc/link.html
# <form method="POST" action="{% url 'cclog:updatelink' %}">
# @login_required(login_url='login')	#	login → url name
def updatelink( request ):
	vendors = get_vendors()

	# from ../models import CC
	c = request.POST['choice']
	print( '**************************************')
	# print ( type ( c ) )
	# print( c )

	pks		= ast.literal_eval( request.POST.get("choice") )
	# pk		= CC_log.objects.get( pk=pks[0] )
	pk		= pks[0]
	cc_id	= pks[1]

	print( f'{request.user.username} update {pk}' )
	qs = Log.objects.filter(pk=pk)
	if not qs.exists():
		return HttpResponse(f'Log { pk } does not exist.  Call or text 925.575.7070.')

	#	Can not use qs from filter → need to use .get
	i		= Log.objects.get( pk=pk )	# Causes matching query does not exist
	t 		= CCm.objects.get( pk=cc_id )
	i.cc_id			= cc_id
	i.cc_id_key		= t

	form	= CC_Log_Form2( instance = i )
	form.fields['log_id'].widget.attrs['readonly'] = True
	form.fields['user_id'].widget.attrs['readonly'] = True

	title			= 'Update Link Log'
	template		= 'cclog/update.html'

	if i.voided:
		title		= 'Log Voided'
		template	= 'cclog/view.html'
		form		= disable( form )

	if i.closed:
		title		= 'Log Closed'
		if not request.user.username in vip:
			template	= 'cclog/view.html'
			form		= disable( form )

	if not request.user.is_superuser:
		if not request.user.username in vip:
			if i.user_id != request.user.username:
				title		= 'Non Purchaser View'
				template	= 'cclog/view.html'
				form		= disable( form )

	context = {
				'title': title,
				'i': i,
				'form': form,
				'vendors': vendors }

	return render( request, template, context )



def disable( form ):
	form.fields['log_id'].widget.attrs['readonly'] = True
	form.fields['user_id'].widget.attrs['readonly'] = True
	# if form.fields['cc_id'].exists:
	# form.fields['cc_id'].widget.attrs['readonly'] = True	#	Not used in add new log
	form.fields['transaction_date'].widget.attrs['readonly'] = True
	form.fields['vendor_id'].widget.attrs['readonly'] = True
	form.fields['vendor_id_key'].widget.attrs['disabled'] = True
	form.fields['vendor'].widget.attrs['readonly'] = True
	form.fields['amount'].widget.attrs['readonly'] = True
	form.fields['ro1'].widget.attrs['readonly'] = True
	form.fields['ro2'].widget.attrs['readonly'] = True
	form.fields['ro3'].widget.attrs['readonly'] = True
	form.fields['ro4'].widget.attrs['readonly'] = True
	form.fields['ro5'].widget.attrs['readonly'] = True
	form.fields['invoice'].widget.attrs['readonly'] = True
	form.fields['returned'].widget.attrs['disabled'] = True
	form.fields['credit'].widget.attrs['disabled'] = True
	form.fields['voided'].widget.attrs['disabled'] = True
	form.fields['closed'].widget.attrs['disabled'] = True
	return form



@login_required(login_url='login')	#	login → url name
def update_save(request, pk):
	from ie.views import cc_clear_links, cc_mark_links
	post_keys = list(request.POST.keys())
	# print( post_keys )
	i = Log.objects.get(pk=pk)
	form = CC_Log_Form3( request.POST, instance = i )		#	9/24/2021 show vendor_id_key

	#	if User.is_superuser:  Does not work
	if request.user.is_superuser or request.user.username in vip:
		# i = link_key( i )
		form = CC_Log_Form3( request.POST, instance = i )
		# print('Superuser → Log Form 2')

	if form.is_valid():
		if form.cleaned_data.get("voided"):
			i.stop	= int( time.time() )

		if form.cleaned_data.get("closed"):
			i.stop	= int( time.time() )

		# 09/21/2021
		if VendorModel.objects.filter(pk=i.vendor_id).exists():
			vid = VendorModel.objects.get( pk=i.vendor_id )
			i.vendor_id_key = vid
			# print( 'saved Update vid today!!!!!!!!!!!')

		i.cc_id = ''
		if i.cc_id_key:
			# print( '317 **************** cc_id_key')
			# print( i.cc_id_key.cc_id )
			# print('**********')
			i.cc_id = i.cc_id_key.cc_id

		form.save()
		# i.save()			#	Save cc_id_key
		# form = CC_Log_Form( instance = i )


		if request.user.is_superuser or request.user.username in vip:
			link_key( i )
			# print('330 superuser')
			form = CC_Log_Form3( instance = i )

			cc_clear_links()		#	Updates cc: user_id ro invoice
			cc_mark_links()		#	Refreshes after each search

		form = disable( form )
		# if 'cc_id' in post_keys:
		# 	form.fields['cc_id'].widget.attrs['disabled'] = True	# Not used in adding a new log
		# 	form.fields['cc_id_link'].widget.attrs['readonly'] = True
		# 	form.fields['po'].widget.attrs['disabled'] = True
		#	cc_id	→ cc_id_key
		if 'cc_id_key' in post_keys:
			# print( '350 ****************************** cc_id_key')
			form.fields['cc_id_key'].widget.attrs['disabled'] = True	# Not used in adding a new log
			form.fields['cc_id'].widget.attrs['readonly'] = True
			form.fields['po'].widget.attrs['disabled'] = True

		title	= 'Update Saved'		#	status confirmation
		template = 'cclog/view.html'
		context = {
				'title': title,
				'form': form,
					'i': i
		}
		print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user } Updated & Saved Log { i }' )
		return render( request, template, context )

	else:
		print('Form Not Valid')
		print(form.errors)
		return HttpResponse('Error detected.')


def get_post(request):
	s = ""
	for key in request.POST:
		value = request.POST[key]
		s += key + ':' + value + '<br>'

	return s


@login_required(login_url='login')	#	login → url name
def reopen(request, pk):
	print('reopen')
	i = Log.objects.get(pk=pk)
	i.closed = False				#		Admin override
	i.stop	= 1
	i.save()
	# print( i )
	form = CC_Log_Form( instance = i )
	form = disable( form )
	title	= 'Update Saved'		#	status confirmation
	template = 'cclog/view.html'
	context = {
			'title': title,
			'form': form,
				'i': i
	}
	return render( request, template, context )



def whoami( request ):
	return HttpResponse( f'Hello {request.user.username} !' )

# Deprecated No search filter
# # @login_required(login_url='login')	#	login → url name
# def logs( request ):
# 	cursor = connection.cursor()
# 	t = timestamp	= int( time.time() )
# 	cursor.execute(f"select log_id, user_id, transaction_date, vendor, debit, amount, ro1, invoice, returned, voided, closed, cc_id, start, stop FROM cclog_cc_log" )
# 	results = cursor.fetchall()
# 	context =	{	'transactions': results,
# 					'count':		len( results)
# 				}
# 	return render( request, 'cclog/logs.html', context )


def help( request ):
		template = 'cclog/help.html'
		context = { }

		return render( request, template, context )




#	08/07/2021
# https://www.codingforentrepreneurs.com/blog/django-tutorial-get-list-of-current-users
# from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)


def currentusers( request ):
	queryset = get_current_users()
	print( len( queryset ))
	cusers = []
	s = ''
	for i in queryset:
		cusers.append( str( i ) )
		s += str( i ) + '<br>'
		print( i )


	# print(queryset.exists())
	print( queryset.count() )
	print( cusers )
	# return HttpResponse( f'{ queryset.count() }' )
	# return HttpResponse( f'{ cusers }' )
	return HttpResponse( f'{ s }' )
