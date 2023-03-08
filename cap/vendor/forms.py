from django import forms
from vendor.models import VendorModel

class Vendor_Form( forms.ModelForm ):
	class Meta:
		model = VendorModel
		fields = ( 'vendor_id', 'name', 'alias', 'address', 'city', 'state', 'zip', 'firstname', 'lastname', 'phone', 'email', 'type' )
