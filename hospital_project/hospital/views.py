from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Doctor
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

def home(request):
    return render(request, "home.html")


def patient(request):
    if request.method == "POST":
        if "register" in request.POST:
        
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            phone = request.POST.get("phone")
            dob = request.POST.get("dob")
            gender = request.POST.get("gender")
            blood_group = request.POST.get("blood_group")
            medical_history = request.POST.get("medical_history")
            address = request.POST.get("address")

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
def doctor(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        doctor_exists = Doctor.objects.filter(email=email).first()
        

        if doctor_exists:        
            if check_password(password, doctor_exists.password):
                
                request.session["doctor_name"] = doctor_exists.fullName
                return redirect("doctor_dashboard")
            else:
                messages.error(request, "Invalid password.")
        else:
            messages.error(request, "Doctor not found. Please contact admin.")

    return render(request, "doctor.html")

def doctor_dashboard(request):
    doctor_name = request.session.get("doctor_name", "Doctor")
    return render(request, "doctor-dashboard.html", {"doctor_name": doctor_name})
