from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from po.models import PO
from po.filters import PO_Filter
from datetime import datetime

# @login_required(login_url='login')	#	login → url name
def po( request ):
	print( f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") } { request.user } - View POs' )
	# ro_list = RO.objects.all()
	all = PO.objects.all()		# This needs to be in parenthesis

	filter = PO_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	# cool = len( filter.qs['cost'] )
	cost 	= 0
	price 	= 0
	for i in filter.qs:
		cost	+= i.cost
		price	+= i.price

	# tot = filter.qs.objects.annotate(cost=Sum('cost'))

	context = { 'transactions': filter,
					'count':	n,
					'total_cost': round( cost, 2),
					'total_price': round( price, 2)
					 }
	return render( request, 'po/po.html', context )



@permission_required( 'admin.can_add_log_entry' )
def killpo( request ):
	while PO.objects.count():
		print( PO.objects.count() )
		PO.objects.all()[0].delete()

	all = PO.objects.all()
	n	= PO.objects.count()
	context = { 'transactions': all,
					'count':	n }
	return render( request, 'po/index.html', context )












# 04/01/2021
# @login_required(login_url='login')	#	login → url name
def dups( request ):
	from django.db import connection
	cursor = connection.cursor()
	# cursor.execute("select cc_cc.cc_id, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount, cclog_cc_log.log_id, cclog_cc_log.vendor, cclog_cc_log.amount,   cclog_cc_log.ro1, cclog_cc_log.invoice, cclog_cc_log.user_id FROM cc_cc INNER JOIN cclog_cc_log ON cc_cc.cc_id = cclog_cc_log.cc_id" )
	cursor.execute("SELECT *, COUNT(*) FROM po_po GROUP BY ro, invoice HAVING COUNT(*) > 1 ORDER BY ro" )

	results = cursor.fetchall()
	context = { 'transactions': results,
				'count':		len( results) }
	return render( request, 'po/sql.html', context )
