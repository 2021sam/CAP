from cc.models import CCm
import django_filters

class CC_Filter( django_filters.FilterSet ):
	posted_date	= django_filters.CharFilter(lookup_expr='icontains')
	payee	 	= django_filters.CharFilter(lookup_expr='icontains')
	address	 	= django_filters.CharFilter(lookup_expr='icontains')
	amount		= django_filters.CharFilter(lookup_expr='icontains')
	# log_id__gt	= django_filters.NumberFilter( field_name='log_id', lookup_expr='gt' )

	# class Meta:
	# 	model = CC
	# 	fields = ['log_id__gt']		# Exact
