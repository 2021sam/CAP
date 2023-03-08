from django.urls import path
from . import views

app_name	= 'link'
urlpatterns = [
    path( '',       views.ui,   name='ui'  ),
    path('auto', views.auto_link, name='auto_link')
]
