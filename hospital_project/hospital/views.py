from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def add_patient(request):
    return render(request, "templates/patient.html")
