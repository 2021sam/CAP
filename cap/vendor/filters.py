from vendor.models import VendorModel
import django_filters


# class Vendor_Filter( django_filters.FilterSet ):

# 	class Meta:
# 		model = VendorModel
# 		# fields = ['ro', 'invoice', 'vendor']		# Exact
# 		fields = {
# 			'name': ['icontains'],
# 			'alias': ['icontains'],
# 			'address': ['icontains']
# 		}


class Vendor_Filter( django_filters.FilterSet ):
	vendor_id	= django_filters.CharFilter(lookup_expr='exact')
	name	 	= django_filters.CharFilter(lookup_expr='icontains')
	alias	 	= django_filters.CharFilter(lookup_expr='icontains')
	address	 	= django_filters.CharFilter(lookup_expr='icontains')
	city		= django_filters.CharFilter(lookup_expr='icontains')
