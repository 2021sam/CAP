from django.db import models
from cc.models import CCm
from po.models import PO
from vendor.models import VendorModel

class Log( models.Model ):
	log_id				=	models.IntegerField( default = 0 )
	user_id				=	models.CharField( max_length = 15, default = '', blank=True )
	cc_id				=	models.CharField( max_length = 23, default = '', blank=True )	#	Reference
	cc_id_key			=	models.ForeignKey( CCm, on_delete=models.SET_NULL, blank=True, null=True )
	# po_id_link			=	models.IntegerField( default = 0 )
	po					=	models.ManyToManyField( PO, blank=True, null=True )
	transaction_date	=	models.DateField()
	vendor_id			=	models.IntegerField( default = 0 )
	vendor_id_key		=	models.ForeignKey( VendorModel, on_delete=models.SET_NULL, blank=True, null=True )
	vendor				=	models.CharField( max_length = 50, default = '' )			# payee → CC payee
	amount				=	models.FloatField( blank=True, null=True )
	ro1					=	models.IntegerField( default=0, blank=True, null=True )
	ro2					=	models.IntegerField( default=0, blank=True, null=True )
	ro3					=	models.IntegerField( default=0, blank=True, null=True )
	ro4					=	models.IntegerField( default=0, blank=True, null=True )
	ro5					=	models.IntegerField( default=0, blank=True, null=True )
	invoice				=	models.CharField( max_length = 20, default = '', blank=True )
	returned			=	models.BooleanField( default = False )
	credit				=	models.BooleanField( default = False )
	voided				=	models.BooleanField( default = False )
	closed				=	models.BooleanField( default = False )

	po_cost				= models.FloatField( blank=True, null=True )
	po_price			= models.FloatField( blank=True, null=True )

	start				=	models.IntegerField( default = 0 )
	stop				=	models.IntegerField( default = 0 )			# epoch


	def __str__(self):
		return f'{ self.log_id } { self.user_id } {self.cc_id_key} {self.transaction_date} {self.vendor_id} {self.vendor} {self.amount} {self.ro1} {self.ro2} {self.ro3} {self.ro4} {self.ro5} {self.invoice} {self.returned} {self.credit} {self.voided} {self.closed} {self.start} {self.stop}'
