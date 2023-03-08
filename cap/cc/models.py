# import datetime
from datetime import date
from django.db import models

class CCm( models.Model ):
	cc_id				=	models.CharField( max_length = 23, primary_key = True )	#	Reference
	up_id				=	models.CharField( max_length = 15, default = '' )
	user_id				=	models.CharField( max_length = 15, default = '', blank=True )
	claim_timestamp		=	models.IntegerField( default = 0 )			# epoch
	posted_date			=	models.DateField( )
	payee				=	models.CharField( max_length = 50 )
	address				=	models.CharField( max_length = 20 )
	amount				=	models.FloatField( )
	log_id				=	models.IntegerField( default = 0 )
	ro					=	models.CharField( max_length = 100, default = '', blank=True )
	invoice				=	models.CharField( max_length = 20, default = '', blank=True )
	# date				=	models.DateField( default=date.today )

	def __str__(self):
		# s = f'{ self.ro_id } { self.date: <10} { self.ro } { self.invoice: <20} { self.category: <20} { self.vendor: <30} { self.cost: < 10}'
		# return f'{ self.cc_id } { self.ro_id } {self.posted_date} {self.payee} {self.address} {self.amount} {self.ro} {self.invoice}'
		return f'{ self.cc_id } {self.posted_date} {self.payee} {self.address} {self.amount}'
