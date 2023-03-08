from django.urls import path
from . import views

app_name	= 'mail'
urlpatterns = [
	path('',		views.email, 		name='email'),
	path('a/',		views.email_attach, name='email_attach')
]
