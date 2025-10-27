from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages  # ✅ Import messages
from .models import Patient
# ----------------------------
# 🏠 HOME PAGE
# ----------------------------
def home(request):
    return render(request, "home.html")


#  PATIENT SECTION
def patient(request):
    if request.method == "POST":
        # Registration Form Submission
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        medical_history = request.POST.get("medical_history")
        address = request.POST.get("address")

        # Save to database
        Patient.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone,
            dob=dob,
            gender=gender,
            blood_group=blood_group,
            medical_history=medical_history,
            address=address
        )
        messages.success(request, "Patient registered successfully!")
        return redirect("patient")

    return render(request, "patient.html")

# Login View
def patient_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check credentials
        try:
            patient = Patient.objects.get(email=email, password=password)
            request.session["patient_name"] = patient.name
            return redirect("patient_dashboard")
        except Patient.DoesNotExist:
            messages.error(request, "Invalid Email or Password.")
            return redirect("patient_login")

    return render(request, "patient-login.html")


def patient_dashboard(request):
    patient_name = request.session.get("patient_name", "Patient")
    return render(request, "patient-dashboard.html", {"patient_name": patient_name})


# ----------------------------
# 👨‍⚕️ DOCTOR SECTION
def doctor(request):
    if request.method == "GET":
        return render(request, "doctor.html")

    email = request.POST.get("email")
    password = request.POST.get("password")

    if email == "r1@gmail.com" and password == "10":
        request.session["doctor_name"] = " aayushi "  # ✅ store temporarily
        return redirect("doctor_dashboard")
    else:
        messages.error(request, "Invalid Email or Password.")
        return render(request, "doctor.html")


def doctor_dashboard(request):
    doctor_name = request.session.get("doctor_name", "Doctor")
    return render(request, "doctor-dashboard.html", {"doctor_name": doctor_name})


