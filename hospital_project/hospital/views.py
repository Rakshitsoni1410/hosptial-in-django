from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages  # ✅ Import messages

# ----------------------------
# 🏠 HOME PAGE
# ----------------------------
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
        request.session["patient_name"] = "Ravi"  # Save name in session
        return redirect("patient_dashboard")
    else:
        messages.error(request, "Invalid Email or Password.")
        return render(request, "patient.html")


def patient_dashboard(request):
    # ✅ Retrieve stored session name (default fallback)
    patient_name = request.session.get("patient_name", "Patient")
    context = {"patient_name": patient_name}
    return render(request, "patient-dashboard.html", context)


# ----------------------------
# 👨‍⚕️ DOCTOR SECTION
# ----------------------------
def doctor(request):
    if request.method == "GET":
        return render(request, "doctor.html")

    email = request.POST.get("email")
    password = request.POST.get("password")

    if email == "r1@gmail.com" and password == "10":
        request.session["doctor_name"] = "Dr. Smith"  # ✅ store temporarily
        return redirect("doctor_dashboard")
    else:
        messages.error(request, "Invalid Email or Password.")
        return render(request, "doctor.html")


def doctor_dashboard(request):
    doctor_name = request.session.get("doctor_name", "Doctor")
    return render(request, "doctor-dashboard.html", {"doctor_name": doctor_name})


