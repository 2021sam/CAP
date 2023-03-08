from django.db import models

class RO( models.Model ):
	ro_id		= models.IntegerField( primary_key = True )
	up_id		= models.CharField( max_length = 15, default = '' )
	date 		= models.CharField( max_length = 10 )
	ro 			= models.IntegerField()
	invoice		= models.CharField( max_length = 20 )
	category	= models.CharField( max_length = 10 )
	vendor		= models.CharField( max_length = 30 )
	qty			= models.CharField( max_length = 1  )
	price		= models.FloatField()
	cost		= models.FloatField()
	transferred	= models.CharField( max_length = 1 )
	payables	= models.CharField( max_length = 1 )
	credit		= models.CharField( max_length = 1 )
	voided		= models.CharField( max_length = 1 )
	closed		= models.CharField( max_length = 1 )


	def __str__(self):
		# return str( self.ro_id ) + ' ' + self.date + ' ' + str( self.ro ) + ' ' + self.invoice + ' ' + self.category + ' ' + self.vendor + ' ' + str( self.cost )
		# return f"{ self.ro_id } { self.date:*<10 } { self.ro:*<10 } { self.invoice:*<15 } { self.category:*<10 } { self.vendor } { self.cost }"
		
		# s = f'{ self.ro_id } { self.date:*<10 } { self.ro } { self.invoice:*<15 } { self.category:*<10 } { self.vendor } { self.cost }'
		# s = f'{ self.ro_id:*<10 }'
		# s = f'{self.date:*<10}'


		# s = f'{self.date:*<10 }'
		s = f'{ self.ro_id } { self.date: <10} { self.ro } { self.invoice: <20} { self.category: <20} { self.vendor: <30} { self.cost: < 10}'
		return s
