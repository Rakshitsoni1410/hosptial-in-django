from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home,path='home.html'),
    path('add_patient/', views.add_patient,path='patient.html'),
]
