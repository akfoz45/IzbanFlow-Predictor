from django.contrib import admin
from django.urls import path
from .views import predict_density_api, index_view

urlpatterns = [
    path('predict/', predict_density_api, name='predict_density_api'),
    path('', index_view, name='index_view')
]