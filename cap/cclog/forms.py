from django import forms
from cclog.models import Log

class CC_New_Log_Form( forms.ModelForm ):
	class Meta:
		model 	= Log
		#	sans voided, could add user_id & disable.
		fields	= [									'transaction_date', 'vendor_id', 'vendor', 'amount', 'ro1', 'ro2', 'ro3', 'ro4', 'ro5', 'invoice', 'returned', 'credit', 		  'closed']
		

	# def __init__( self, *args, **kwargs ):
	# 	super().__init__( *args, **kwargs )
	# 	self.fields['vendor'].queryset = ['a', 'b', 'c', 'qbert']


class CC_Log_Form( forms.ModelForm ):
	class Meta:
		model 	= Log
		fields	= ['log_id', 'user_id', 							'transaction_date', 'vendor_id', 'vendor_id_key', 'vendor', 'amount', 'ro1', 'ro2', 'ro3', 'ro4', 'ro5', 'invoice', 'returned', 'credit', 'voided', 'closed']


class CC_Log_Form2( forms.ModelForm ):
	class Meta:
		model 	= Log
		fields	= ['log_id', 'user_id', 'cc_id', 'cc_id_key', 'po', 'transaction_date', 'vendor_id', 'vendor', 'amount', 'ro1', 'ro2', 'ro3', 'ro4', 'ro5', 'invoice', 'returned', 'credit', 'voided', 'closed']


class CC_Log_Form3( forms.ModelForm ):
	class Meta:
		model 	= Log
		fields	= ['log_id', 'user_id', 'cc_id', 'cc_id_key', 'po', 'transaction_date', 'vendor_id', 'vendor_id_key', 'vendor', 'amount', 'ro1', 'ro2', 'ro3', 'ro4', 'ro5', 'invoice', 'returned', 'credit', 'voided', 'closed']
