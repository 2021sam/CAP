from po.models import PO
import django_filters


class PO_Filter( django_filters.FilterSet ):

	# CHOICES = [
	# 	('ascending', 'Ascending')
	# 	('descending', 'Descending')
	# ]
	# ordering = django_filters.ChoiceFilter( label='Ordering', choices=CHOICES, method='filter_by_order' )

	class Meta:
		model = PO
		# fields = ['ro', 'invoice', 'vendor']		# Exact
		fields = {
			'ro': ['icontains'],
			'invoice': ['icontains'],
			'vendor': ['icontains']
		}