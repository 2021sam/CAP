from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from cc.models import CCm
from cclog.models import Log
from vendor.models import VendorModel
from django.db import connection


# @periodic_task(run_every=crontab(minute=0, hour='6,18'))
def auto_link( request ):
	cc_days_back	= 30
	offset_days		= 15
	context = ui_post( cc_days_back, offset_days )
	print( context )
	return render( request, 'link/histogram.html', context )


def ui( request ):
	template	= 'link/link.html'
	if request.method == 'GET':
		return render( request, template, {} )

	if request.method == "POST":
		print('Post')
		post_keys = list(request.POST.keys())
		print( f'Post: { post_keys}' )
		cc_days_back	= int( request.POST.get("cc_days_back") )
		offset_days		= int( request.POST.get("offset_days") )

	context = ui_post( cc_days_back, offset_days )
	return render( request, 'link/histogram.html', context )


def ui_post( cc_days_back, offset_days ):
	import datetime
	import time

	today = datetime.datetime.today()
	vendors = VendorModel.objects.filter( inactive=False )
	# for v in vendors:
	# 	print( v )
	common = ['CA', 'HAYWARD', 'INC']
	startdate = today - datetime.timedelta( days= cc_days_back )
	cc = CCm.objects.filter( log_id=0, posted_date__range=[startdate, today] )
	n = len( cc )
	d = {}
	cost = 0
	for i in cc:
		if i.amount > 0:
			cost	+= i.amount

	for i in cc:
		startdate = i.posted_date - datetime.timedelta(days = offset_days )
		enddate  = i.posted_date + datetime.timedelta(days = offset_days )
		# print( f'Start → End: { startdate } → { i.posted_date } → { enddate }')
		log = Log.objects.filter( transaction_date__range=[ startdate, enddate ], cc_id__exact='' )

		for j in log:
			# print( j )

			if j.amount:
				# print( f'CC: = { i.date } { i.payee } { i.amount }: → LOG: { j.transaction_date } { j.amount }' )
				a = int( i.amount * 100 )
				b = int( j.amount * 100 )

				if a == b:
					# if j.id == 457:
					# 	print( j )
					# 	print( f'j.vendor_id { j.vendor_id }' )
					name_alias = j.vendor
					if j.vendor_id:
						v = vendors.get( pk = j.vendor_id )
						# print( f'******** {v}' )
						s = v.alias
						alias = s.replace(',', '')
						name_alias = j.vendor + ' ' + alias
						# print( f'92 ***** {name_alias}')

					print( f'CC: ={ i.log_id } {i.posted_date } { i.payee } { i.amount }: → LOG: { j.transaction_date } {j.vendor_id} { j.vendor } {name_alias} { j.amount }' )
					cc_vendorarray	= i.payee.split()
					# log_vendorarray = j.vendor.split()
					log_vendorarray = name_alias.split()

					match = False
					for k in log_vendorarray:
						if match:
							break
			
						if k in common:
							continue

						for m in cc_vendorarray:
							if k == m:
								print( f'Match: {i.log_id} {k} = {m}')
								i.log_id = j.log_id
								i.save()

								j.cc_id	= i.cc_id
								j.cc_id_key		= i
								j.save()
								match = True

								delta = i.posted_date - j.transaction_date
								print( f'delta.days = { delta.days }' )

								if not delta.days in d.keys():
									d[ delta.days ] = 1
								else:
									d[ delta.days ] += 1

								break

	context =	{
					'cc_days_back': cc_days_back,
					'offset_days': offset_days,
					'transactions': cc,
					'count':	n,
					'd': d
				}

	return context


# def Coolthisup():
# 	#	Can not use qs from filter → need to use .get
# 	# i		= Log.objects.get( pk=pk )	# Causes matching query does not exist
# 	# t 		= CCm.objects.get( pk=cc_id )
# 	i.cc_id_link	= cc_id
# 	i.cc_id			= t

# 	form	= CC_Log_Form2( instance = i )
# 	form.fields['log_id'].widget.attrs['readonly'] = True
# 	form.fields['user_id'].widget.attrs['readonly'] = True

# 	title			= 'Update Link Log'
# 	template		= 'cclog/update.html'



def cc_sql( request ):
	# print('cc_mark_linked()')
	cursor = connection.cursor()
	# cursor.execute("select cc_cc.cc_id, cclog_cc_log.user_id, cclog_cc_log.log_id, cclog_cc_log.ro1, cclog_cc_log.invoice FROM cc_cc INNER JOIN cclog_cc_log ON cc_cc.cc_id = cclog_cc_log.cc_id" )
	# cursor.execute("select cc_ccm.cc_id, cclog_cc_log.user_id, cclog_cc_log.log_id, cclog_cc_log.ro1, cclog_cc_log.invoice FROM cc_ccm INNER JOIN cclog_cc_log ON cc_ccm.cc_id = cclog_cc_log.cc_id_link" )
	# cursor.execute("select cc_ccm.cc_id, cclog_log.user_id, cclog_log.log_id, cclog_log.ro1, cclog_log.invoice FROM cc_ccm INNER JOIN cclog_log ON cc_ccm.cc_id = cclog_log.cc_id_link" )
	cursor.execute( "select * FROM cc_CCm" )
	results = cursor.fetchall()
	print( '41 Got Results')

	# for i in results:
	# 	print( f'i = { i }')
	# 	pk = i[0]
	# 	qs = CCm.objects.filter(pk = pk)
	# 	if not qs.exists():
	# 		return HttpResponse(f'CC { pk } does not exist.  Call or text 925.575.7070.')
	# return HttpResponse('Done.')
	n = len( results )
	cost = 0
	# for i in filter.qs:
	# 	cost	+= i.amount

	context =	{
					'link': False,
					'transactions': results,
					'count':	n,
					'total_cost': round( cost, 2)
				}
	return render( request, 'link/viewsql.html', context )



# def ccdate( request ):
# 	import datetime
# 	format_str = '%m/%d/%Y'
# 	all = CCm.objects.filter()

# 	# all = Log.objects.filter( )
# 	for i in all:
# 		if i.posted_date:
# 			print( f'{i.posted_date}')
# 			i.date = datetime.datetime.strptime(i.posted_date, format_str)	
# 			i.save()
# 			if i.date.month > 4:
# 				i.delete()

# 	return HttpResponse('Date conversion')