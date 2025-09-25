from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('patient/', views.patient),
    path('doctor/',views.doctor)
]
