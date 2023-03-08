# https://www.youtube.com/watch?v=BppyfPye8eo

from django import forms
from cc.models import CCm

class CC_Form( forms.ModelForm ):
	class Meta:
		model = CCm
		payee = forms.CharField( disabled = True )
		fields = ['posted_date', 'cc_id', 'payee', 'address', 'amount', 'ro', 'invoice']


class CC_Update_Form( forms.ModelForm ):
	class Meta:
		model = CCm
		fields = ['ro', 'invoice']
