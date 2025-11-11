from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Patient
    path('patient/', views.patient, name='patient'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    # Doctor
    path('doctor/', views.doctor, name='doctor'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
