# https://www.youtube.com/watch?v=BppyfPye8eo

# from django.shortcuts import render
# from ro.models import RO
# from ro.forms import RO_Form
# import csv, io							#	file
# from django.contrib import messages		#	file
# from django.contrib.auth.decorators import permission_required	# file
# from ro.filters import RO_Filter

# def index( request ):
# 	# now = datetime.datetime.now()
# 	all = RO.objects.all
# 	n = RO.objects.count()
# 	print ( all )
# 	context = { 'transactions': all,
# 					'count':	n }
# 	return render( request, 'ro/index.html', context )



# def ro_form( request ):
# 	template = "ro/form_post.html"

# 	if request.method == "POST":
# 		form = RO_Form( request.POST )
# 		if form.is_valid():
# 			form.save()
	
# 	else:
# 		form = RO_Form()

# 	context = {
# 		'form': form
# 	}
# 	return render( request, template, context )

