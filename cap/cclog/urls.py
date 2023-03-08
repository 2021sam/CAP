from django.urls import path
from . import views

app_name	= 'cclog'
urlpatterns = [
	path('log/',					views.log,			name ='log'	  ),
	path('',						views.logs,			name ='logs'  ),
	path('ll',						views.logs2,		name ='logs2'  ),
	path('update/',					views.update,		name ='update'),
	path('update-save/<int:pk>',	views.update_save,	name ='update_save'),
	path('reopen/<int:pk>',			views.reopen,		name ='reopen' ),
	path('updatelink/',				views.updatelink,	name ='updatelink'),
	path('help/',			views.help,			name='help'),
	path('whoami/',			views.whoami, 		name='whoami'),
	path('currentusers/',				views.currentusers,		name='currentusers')
]
