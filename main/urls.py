from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='index-load'),
    path('base', views.base,name='base'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dash'),
    path('view', views.view, name='view'),
    path('submit', views.submit, name='submit'),
    path('code', views.code, name='code'),
    path('result', views.result, name='result'),
    path('contact', views.contact, name='contact')
]