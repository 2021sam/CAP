from django.urls import path
from . import views

app_name	= 'po'
urlpatterns = [
	path('killpo/', views.killpo, name='killpo'),
	path('',	views.po,	name ='po'),
	path('dups/',	views.dups,		name='dups')
]
