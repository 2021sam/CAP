from django.urls import path
from . import views

app_name	= 'ie'
urlpatterns = [
	path('upload/',			views.upload,		name='upload'  ),
	# path('upload/auto',		views.auto_upload,	name='auto_upload'  ),
	path('download/log/',	views.download_log,	name='download_log'),
	path('cckey/',		views.link_cc_key, 	name='link_cc_key'),
	path('pokey/',		views.link_po_key, 	name='link_po_key'),
	path('linker/',		views.linker,		name='linker')
]
