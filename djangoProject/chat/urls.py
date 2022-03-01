from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('index', views.index, name='index'),
    path('create', views.create, name='create'),
    path('forget', views.forget, name='forget'),
    path('logout', views.logout, name='logout'),

]
