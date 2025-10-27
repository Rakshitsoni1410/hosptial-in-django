from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages  # ✅ Import messages

def home(request):
    return render(request, "home.html")

def patient(request):
    if request.method == "GET":
        return render(request, "patient.html")

    # Get form data
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Dummy login check
    if email == "r@gmail.com" and password == "11":
        return redirect("patient_dashboard")
    else:
        # ✅ Use Django messages to show alert
        messages.error(request, "Invalid Email or Password.")
        return render(request, "patient.html")

def patient_dashboard(request):
    return render(request, "patient-dashboard.html")

def doctor(request):
    return render(request, "doctor.html")
