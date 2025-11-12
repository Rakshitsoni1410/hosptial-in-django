from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    # Patient
    path('patient/', views.patient, name='patient'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    # Doctor
    path('doctor/', views.doctor, name='doctor'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

]
