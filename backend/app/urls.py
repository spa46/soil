from django.urls import path, include
from app import views

urlpatterns = [
    # The home page
    path('', views.index, name='home')
]
