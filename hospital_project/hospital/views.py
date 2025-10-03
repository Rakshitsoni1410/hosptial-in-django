from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    return render(request, "home.html")
def patient(request):
    if request.method == "GET":
        # Just show the login page
        return render(request, "patient.html")

    # Handle POST request (login form submit)
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Dummy authentication check
    if email == "r@gmail.com" and password == "11":
        # Redirect to dashboard (use URL name or template)
        return redirect("/patient-dashboard/")  # or redirect('patient_dashboard')
    else:
        return HttpResponse("Invalid User")
def doctor(request):
    return render(request,"doctor.html")
