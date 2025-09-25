from django.contrib import admin
from django.urls import path,include
from hospital import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('hospital.urls')),
]
