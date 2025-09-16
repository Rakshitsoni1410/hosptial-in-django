from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('appointment/', views.appointment, name='appointment'),
    path('report/', views.report, name='report'),
]
