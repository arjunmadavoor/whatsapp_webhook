from django.urls import path
from .views import *

handler404 = 'dashboard.views.handler404'


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('all_users/', all_users, name='all_users'),
]
