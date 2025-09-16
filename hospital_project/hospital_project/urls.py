from django.contrib import admin
from django.urls import path
from hospital import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('appointment/', views.appointment, name='appointment'),
    path('report/', views.report, name='report'),
]
