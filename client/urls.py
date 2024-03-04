from django.urls import path

from .views import *


urlpatterns = []

GENERAL_URLS = [
    path('login/', client_login, name='login'),
    path('logout/', client_logout, name='logout'),
    path('register/', client_register, name='register'),

]

urlpatterns += GENERAL_URLS