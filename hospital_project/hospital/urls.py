from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('patient/', views.patient, name="patient"),
    path('doctor/', views.doctor, name="doctor"),
    path('patient-dashboard/', views.patient_dashboard, name="patient_dashboard"),
]
