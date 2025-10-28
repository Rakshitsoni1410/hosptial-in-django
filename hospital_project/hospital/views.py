from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient


def home(request):
    return render(request, "home.html")


def patient(request):
    # Handle Registration and Login in same view
    if request.method == "POST":
        if "register" in request.POST:
            # Registration form
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            phone = request.POST.get("phone")
            dob = request.POST.get("dob")
            gender = request.POST.get("gender")
            blood_group = request.POST.get("blood_group")
            medical_history = request.POST.get("medical_history")
            address = request.POST.get("address")

            # Check duplicate email
            if Patient.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                Patient.objects.create(
                    name=name,
                    email=email,
                    password=password,
                    phone=phone,
                    dob=dob,
                    gender=gender,
                    blood_group=blood_group,
                    medical_history=medical_history,
                    address=address,
                )
                messages.success(request, "Registration successful! Please log in.")
            return redirect("patient")

        elif "login" in request.POST:
            # Login form
            email = request.POST.get("login_email")
            password = request.POST.get("login_password")

            try:
                patient = Patient.objects.get(email=email, password=password)
                request.session["patient_name"] = patient.name
                return redirect("patient_dashboard")
            except Patient.DoesNotExist:
                messages.error(request, "Invalid Email or Password.")
                return redirect("patient")

    return render(request, "patient.html")


def patient_dashboard(request):
    patient_name = request.session.get("patient_name", "Patient")
    return render(request, "patient-dashboard.html", {"patient_name": patient_name})
