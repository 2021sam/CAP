from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from cc import views as cc_views

urlpatterns = [
    path( 'admin/', admin.site.urls ),
    path('', auth_views.LoginView.as_view(template_name='cc/login.html'), name='login'),
    path('home', cc_views.home, name='home' ),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout'), name='logout'),
    path('ie/', include('ie.urls')),
    path('mail/', include('mail.urls')),
    path('cc/', include('cc.urls')),
    path('cclog/', include('cclog.urls')),
    path('po/', include('po.urls')),
    path('ro/', include('ro.urls')),
    path('vendor/', include('vendor.urls')),
    path('link/', include('link.urls'))
]
