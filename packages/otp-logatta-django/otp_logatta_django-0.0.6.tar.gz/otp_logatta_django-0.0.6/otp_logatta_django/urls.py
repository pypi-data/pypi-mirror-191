# in urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.request_otp), # new
    path('verify/', views.verify_otp), # new
]  