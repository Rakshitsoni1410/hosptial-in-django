from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('patient/', views.patient, name='patient'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor, name='doctor'),  
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # 👈 dashboard after login
]
