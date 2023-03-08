# https://www.youtube.com/watch?v=BppyfPye8eo
import csv, io, ast, time, datetime, django_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
from cc.models import CCm
from po.models import PO
from cc.forms import CC_Form, CC_Update_Form
from django.contrib.auth.decorators import permission_required
from django.db import connection
from cclog.models import Log
from django.contrib.auth.models import User
from vendor.models import VendorModel
from django.core.mail import send_mail


def home( request ):
	return render( request, 'ie/home.html', {} )

def get_post(request):
	s = ""
	for key in request.POST:
		value = request.POST[key]
		s += key + ':' + value + '<br>'

	return s


# # @permission_required( 'admin.can_add_log_entry' )
# def auto_upload( request ):
# 	# print( f'[{request.user}]' )
# 	template	= 'ie/upload.html'


# 	# with open( '/home/pi/Downloads/currentTransaction_4362.csv', 'r') as csvfile:
# 	# csv_file = open( '/home/pi/Downloads/currentTransaction_4362.csv' )
# 	csv_file = open( '//home//pi//Downloads//currentTransaction_4362.csv' )
# 	csv_file = open( '//home//pi//Downloads//currentTransaction_4362.csv' )
# 	data_set = csv_file.read().decode('UTF-8')
# 	io_string = io.StringIO( data_set )
# 	i_old, i_new = import_cc( request, io_string )
# 	message = 'Credit Card'

# 	context =	{
# 					'computer_nerd': str( request.user ),
# 					'message': message,
# 					'i_old': i_old,
# 					'i_new': i_new
# 				}
# 	return render( request, template, context )



















# @permission_required( 'admin.can_add_log_entry' )
def upload( request ):
	# print( f'[{request.user}]' )
	print('upload')
	template	= 'ie/upload.html'
	if request.method == 'GET':
		return render( request, template, {} )

	if request.FILES.get('file') == None:
		context = { 'message': 'You did not select a file.'}
		return render( request, template, context )

	csv_file = request.FILES['file']

	print( csv_file )

	if not csv_file.name.endswith('.csv'):
		context = { 'message': 'This is not a csv file.'}
		return render( request, template, context )

	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO( data_set )
	# next( io_string )		#	To skip the first record.

	cool = request.POST.get('up_type')
	print( cool )
	if cool == None:
		context = {
			'message': 'You did not select a data structure type.'
		}
		return render( request, template, context )

	if request.POST['up_type'] == 'user':
		message = 'User'
		print( 'You selected User')
		i_old, i_new = import_user( request, io_string )

	if request.POST['up_type'] == 'log':
		message = 'Log'
		print( 'You selected Log')
		i_old, i_new = import_log( request, io_string )

	if request.POST['up_type'] == 'po':
		message = 'Purchase Order'
		print( 'You selected Purchase Order')
		i_old, i_new = import_po( request, io_string )
	
	if request.POST['up_type'] == 'cc':
		message = 'Credit Card'
		print( 'You selected Credit Card')
		i_old, i_new = import_cc( request, io_string )


	# 09/19/2021
	if request.POST['up_type'] == 'vendor':
		message = 'Vendor'
		print( 'You selected Vendor')
		i_old, i_new = import_vendor( request, io_string )


	context =	{
					'computer_nerd': str( request.user ),
					'message': message,
					'i_old': i_old,
					'i_new': i_new
				}
	return render( request, template, context )




def import_user( request, io_string ):
	next( io_string )		#	To skip the first record.
	i_new = 0
	i_old = 0
	status = ''

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		i	= User(
			username	= column[0],
			password	= column[1],
			first_name	= column[2],
			email		= column[3]
			)

		i.set_password( column[1] )

		if User.objects.filter(username=i.username).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )

	return i_old, i_new



def import_log( request, io_string ):
	i_new = 0
	i_old = 0
	status = ''

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		i	= Log(
			log_id			= column[0],
			user_id			= column[1],
			cc_id			= column[2],
			transaction_date= column[3],
			vendor_id		= column[4],
			vendor			= column[5],
			amount			= (column[6], 0)[not column[6]],
			ro1				= (column[7], 0)[not column[7]],
			ro2				= (column[8], 0)[not column[8]],
			ro3				= (column[9], 0)[not column[9]],
			ro4				= (column[10], 0)[not column[10]],
			ro5				= (column[11], 0)[not column[11]],

			invoice			= column[12],
			returned		= column[13],
			credit			= column[14],
			voided			= column[15],
			closed			= column[16],
			start			= column[17],
			stop			= column[18]
			)


		if Log.objects.filter(pk=i.id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )

	# all = CC_log().objects.all()
	mia	= []
	all = Log.objects.filter( )
	for i in all:
		print( f'{i.id} → {i.log_id}')
		i.log_id = i.id
		i.save()

	print( f'The following are cc_ids that are MIA in the CC table:')
	print( mia )

	return i_old, i_new




def import_po( request, io_string ):
	while PO.objects.count():
		# print( PO.objects.count() )
		PO.objects.all()[0].delete()

	i_new = 0
	i_old = 0
	status = ''
	next( io_string )		#	To skip the first record.

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		i = PO(
			po_id		= column[12],
			up_id		= request.user,
			date		= column[0],
			ro			= column[1],
			invoice		= column[2],
			category	= column[3],
			vendor		= column[4],
			qty			= column[5],
			price		= float( column[6].replace(',','') ),
			cost		= float( column[7].replace(',','') ),
			transferred	= column[8],
			payables	= column[9],
			credit		= column[10],
			voided		= column[11],
			closed		= column[19]
		)

		if PO.objects.filter(pk=i.po_id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )
		# status += s

	return i_old, i_new



def import_cc( request, io_string ):
	next( io_string )		#	To skip the first record.
	i_new = 0
	i_old = 0
	status = ''

	import datetime
	format_str = '%m/%d/%Y'
	# all = CCm.objects.filter()

	# # all = Log.objects.filter( )
	# for i in all:
	# 	if i.posted_date:
	# 		print( f'{i.posted_date}')
			# i.date = datetime.datetime.strptime(i.posted_date, format_str)	


	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		if not column[0]:
			print( 'column[0] is empty' )
			continue

		if column[1] == 'TEMPREV':
			print('TEMPREV')
			continue

		i = CCm(
			cc_id			= column[1],
			up_id			= request.user,
			user_id			= '',
			claim_timestamp = 0,
			posted_date		= datetime.datetime.strptime( column[0], format_str ),
			payee			= column[2],
			address			= column[3],
			amount			= -1 * float( column[4] ),
			ro 				= '',
			invoice			= ''
		)

		if CCm.objects.filter(pk=i.cc_id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )
		# status += s

	return i_old, i_new






#	09/19/2021
def import_vendor( request, io_string ):
	next( io_string )		#	To skip the first record.
	i_new = 0
	i_old = 0
	status = ''

	# load_vendor_array()
	#	to add alias back during import.

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		i	= VendorModel(
			vendor_id	= column[0],
			name		= column[2],
			address		= column[5],
			city		= column[8],
			state		= column[9],
			zip			= column[10],
			phone		= column[12],
			firstname	= column[18],
			lastname	= column[19],
			alias		= column[20],
			email		= column[21],
			type		= column[23],
			inactive	= column[26]
			)
		

		if VendorModel.objects.filter(pk=i.vendor_id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
			j = VendorModel.objects.get( pk=i.vendor_id )
			j.delete()

			# j.alias = i.alias
			i.save()
	
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )

	return i_old, i_new














def current_datetime(request, message):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.<br>%s</body></html>" % ( now, message )
    return HttpResponse(html)





#	================================================================
#	==========================	DOWNLOADS	========================
#	================================================================

def download_log(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="log.csv"'
	writer = csv.writer(response)

	records = Log.objects.all()
	for i in records.iterator():
		print( i.log_id )
		writer.writerow([ i.log_id, i.user_id, i.cc_id, i.transaction_date, i.vendor_id, i.vendor, i.amount, i.ro1, i.ro2, i.ro3, i.ro4, i.ro5, i.invoice, i.returned, i.credit, i.voided, i.closed, i.start, i.stop ] )
	return response





#	================================================================
#	==========================	LINKER	========================
#	================================================================

# @permission_required( 'admin.can_add_log_entry' )
def linker( request ):
	print( f'[{request.user}]' )
	template	= 'ie/linker.html'
	if request.method == 'GET':
		return render( request, template, {} )

	result = {}
	cool = request.POST.get('link')
	print( cool )
	if cool == None:
		result['Decide'] = 'You did not select a link task.'
		context = {
			'result': result
		}
		return render( request, template, context )

	if request.POST['link'] == '1':
		result = link_cc_key()

	if request.POST['link'] == '2':
		result = link_po_key()

	if request.POST['link'] == '3':
		result = cc_clear_links()

	if request.POST['link'] == '4':
		result = cc_mark_links()

	context =	{
					'computer_nerd': str( request.user ),
					'result': result,
				}
	return render( request, template, context )




#	1
def link_cc_key():
	#	Does not check for cc_id_link != cc_id
	#	Should not be a possiblility
	i_new = 0
	i_old = 0
	i_mia = 0
	mia	= []
	all = Log.objects.filter().exclude( cc_id = '' )
	n = len( all )
	for i in all:
		qs	= CCm.objects.filter( pk=i.cc_id )
		if qs.exists():
			qs	= CCm.objects.get( pk=i.cc_id )
			if i.cc_id:
				i_old += 1

			else:
				# mia.append( i.cc_id_link )
				# print( i.cc_id_link )
				i_new += 1
				i.cc_id_key	= qs
				i.save()

		else:
			i_mia += 1
			mia.append( i.cc_id )

	d = {
		'Old': i_old,
		'New': i_new,
		'MIA': i_mia,
		'Total': n,
		'MIA List': mia
	}

	return d




#	2
def link_po_key():
	#	Does not check for po_id_link != po_id
	#	Should not be a possiblility
	i_new = 0
	i_old = 0
	i_mia = 0
	mia	= []
	all = Log.objects.filter().exclude( ro1 = 0 ).exclude( invoice = '' )
	n = len( all )
	for i in all:
		i.po.clear()
		i.po_cost  = 0
		i.po_price = 0
		i.save()

		qs		= PO.objects.filter( ro = i.ro1, invoice=i.invoice )
		if qs.exists():
			cost = 0
			price = 0
			for j in qs:
				i.po.add( j )
				cost  += j.cost
				price += j.price

				i.po_cost  = round( cost, 2)
				i.po_price = round( price, 2)
				# format( i.po_cost, '.2f' )
				# format( i.po_price, '.2f' )

				i_new += 1
				i.save()

	# s = f'Logs = { n }<br>Old = { i_old }<br>New = { i_new }<br>'
		d = {
		'Logs': n,
		'Old': i_old,
		'New': i_new
	}

	return d


#	3
def cc_clear_links():
	print('Clear CC Links')
	records = CCm.objects.all()
	for i in records.iterator():
		i.user_id	= ''
		i.log_id	= 0
		i.ro		= ''
		i.invoice	= ''
		i.save()
	return {'Clear CC Links': 'Done.'}


#	4
def cc_mark_links():
	# print('cc_mark_linked()')
	cursor = connection.cursor()
	# cursor.execute("select cc_cc.cc_id, cclog_cc_log.user_id, cclog_cc_log.log_id, cclog_cc_log.ro1, cclog_cc_log.invoice FROM cc_cc INNER JOIN cclog_cc_log ON cc_cc.cc_id = cclog_cc_log.cc_id" )
	# cursor.execute("select cc_ccm.cc_id, cclog_cc_log.user_id, cclog_cc_log.log_id, cclog_cc_log.ro1, cclog_cc_log.invoice FROM cc_ccm INNER JOIN cclog_cc_log ON cc_ccm.cc_id = cclog_cc_log.cc_id_link" )
	cursor.execute("select cc_ccm.cc_id, cclog_log.user_id, cclog_log.log_id, cclog_log.ro1, cclog_log.invoice FROM cc_ccm INNER JOIN cclog_log ON cc_ccm.cc_id = cclog_log.cc_id" )
	results = cursor.fetchall()

	for i in results:
		pk = i[0]
		qs = CCm.objects.filter(pk = pk)
		if not qs.exists():
			return HttpResponse(f'CC { pk } does not exist.  Call or text 925.575.7070.')

		#	Can not use qs from filter → need to use .get
		j		= CCm.objects.get( pk=pk )	# Causes matching query does not exist
		j.user_id	= i[1]
		j.log_id	= i[2]
		j.ro		= str( i[3] )
		j.invoice	= i[4]
		j.save()

	return {'Mark CC Links': 'Done.'}


def delete_vendors():
	while VendorModel.objects.count():
		# print( PO.objects.count() )
		VendorModel.objects.all()[0].delete()
