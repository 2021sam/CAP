from django.urls import path
from . import views

app_name	= 'cc'
urlpatterns = [
    path('view/',   views.view, name='view'),
    path('',    views.link,   name='link'   )
]
