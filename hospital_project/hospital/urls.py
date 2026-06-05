from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),

    # Patient
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/appointments/', views.patient_appointments, name='patient_appointments'),
    path('patient/appointments/book/', views.book_appointment, name='book_appointment'),
    path('patient/appointments/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('patient/reports/', views.patient_reports, name='patient_reports'),

    # Doctor
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/appointments/<int:pk>/update/', views.update_appointment, name='update_appointment'),
    path('doctor/appointments/<int:pk>/report/', views.add_report, name='add_report'),
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'),

    # Admin
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/patients/', views.manage_patients, name='manage_patients'),
    path('admin-panel/patients/<int:pk>/delete/', views.delete_patient, name='delete_patient'),
    path('admin-panel/doctors/', views.manage_doctors, name='manage_doctors'),
    path('admin-panel/doctors/<int:pk>/delete/', views.delete_doctor, name='delete_doctor'),
    path('admin-panel/doctors/<int:pk>/toggle/', views.toggle_doctor_availability, name='toggle_doctor_availability'),
    path('admin-panel/appointments/', views.manage_appointments, name='manage_appointments'),
    path('admin-panel/export/pdf/', views.export_reports_pdf, name='export_reports_pdf'),
    path('admin-panel/export/excel/', views.export_reports_excel, name='export_reports_excel'),

    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
]