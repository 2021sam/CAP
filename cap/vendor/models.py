import json
from django.db import models
from django.db.models.fields import EmailField

class VendorModel( models.Model ):
    vendor_id			=	models.IntegerField( max_length = 23, primary_key = True )
    name    			=	models.CharField( max_length = 15, default = '', blank=True )
    alias               =   models.CharField( max_length = 200, blank = True )
    address		        =	models.CharField( max_length = 20, blank = True )
    city	    		=	models.CharField( max_length = 10, blank = True )
    state				=	models.CharField( max_length = 50, blank = True )
    zip	    			=	models.CharField( max_length = 20, blank = True )
    phone               =   models.CharField( max_length = 14, blank = True )
    firstname           =	models.CharField( max_length = 15, blank = True )
    lastname            =	models.CharField( max_length = 15, blank = True )
    email               =   models.EmailField( null = True, blank=True )
    type				=	models.CharField( max_length = 15, blank = True )
    inactive             =   models.BooleanField(  default = False )


# https://stackoverflow.com/questions/22340258/list-field-in-model
    def set_alias(self, x):
        self.alias = json.dumps(x)

    def get_alias(self):
        return json.loads(self.alias)

    def __str__(self):
        return f'{ self.vendor_id } {self.name.ljust(30, "." )} {self.alias.ljust(20, ".")} {self.address.ljust(30, ".")} {self.city.ljust(30, " ")} {self.state.ljust(3, " ")} {self.zip.ljust(10, " ")} {self.firstname.ljust(30, " ")} {self.lastname.ljust(30, " ")} {self.phone.ljust(20, ".")} {self.email.ljust(30, ".")} {self.type}'
