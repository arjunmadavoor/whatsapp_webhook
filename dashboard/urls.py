from django.urls import path
from .views import *

handler404 = 'dashboard.views.handler404'


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('all_users/', all_users, name='all_users'),
    path('registered_users/', registered_users, name='registered_users'),
    path('verified_users/', verified_users, name='verified_users'),
    path('pending_users/', pending_users, name='pending_users'),
    path('verify_user/', verify_user, name='verify_user'),
    path('edit_user/', edit_user, name='edit_user'),
    path('delete_user/', delete_user, name='delete_user'),
    # path('verify_user/<int:user_id>/', verify_user, name='verify_user'),


]
