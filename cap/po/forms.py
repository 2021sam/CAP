from django import forms
from po.models import PO

class PO_Form( forms.ModelForm ):
	class Meta:
		model = PO
		fields = ( 'date', 'ro', 'invoice', 'category', 'vendor', 'qty', 'price', 'cost', 'transferred', 'payables', 'credit', 'voided', 'closed' )
