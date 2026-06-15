from django.contrib import admin
from django.urls import path
from .views import predict_density_api

urlpatterns = [
    path('predict/', predict_density_api, name='predict_density_api'),
]