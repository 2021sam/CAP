from django import forms
from ro.models import RO

class RO_Form( forms.ModelForm ):
	class Meta:
		model = RO
		fields = ( 'date', 'ro', 'invoice', 'category', 'vendor', 'qty', 'price', 'cost', 'transferred', 'payables', 'credit', 'voided', 'closed' )
