from django.shortcuts import render

def home(request):
    return render(request, "base.html")

def add_patient(request):
    return render(request, "add_patient.html")

def add_doctor(request):
    return render(request, "add_doctor.html")

def appointment(request):
    return render(request, "appointment.html")

def report(request):
    return render(request, "report.html")
