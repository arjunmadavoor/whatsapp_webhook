from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.WhatsAppView.as_view(), name='WhatsAppView'),
]
