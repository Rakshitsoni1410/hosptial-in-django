from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages  # ✅ Import messages

def home(request):
    return render(request, "home.html")

# ----------------------------
# 🧍‍♀️ PATIENT SECTION
# ----------------------------
def patient(request):
    if request.method == "GET":
        return render(request, "patient.html")

    # ✅ Get form data (must match input names in HTML)
    email = request.POST.get("email")
    password = request.POST.get("password")

    # ✅ Dummy login check
    if email == "r@gmail.com" and password == "11":
        return redirect("patient_dashboard")
    else:
        messages.error(request, "Invalid Email or Password.")
        return render(request, "patient.html")

def patient_dashboard(request):
    return render(request, "patient-dashboard.html")


# ----------------------------
# 👨‍⚕️ DOCTOR SECTION
# ----------------------------
def doctor(request):
    if request.method == "GET":
        return render(request, "doctor.html")

    email = request.POST.get("email")
    password = request.POST.get("password")

    # ✅ Dummy doctor login check
    if email == "r1@gmail.com" and password == "10":
        return redirect("doctor_dashboard")
    else:
        messages.error(request, "Invalid Email or Password.")
        return render(request, "doctor.html")

def doctor_dashboard(request):
    return render(request, "doctor-dashboard.html")
