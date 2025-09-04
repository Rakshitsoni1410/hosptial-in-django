from django.http import HttpResponse

def home(request):
    return HttpResponse(
        "<h1>🏥 Hospital Management System</h1>"
        "<a href='/add-patient/'>Add Patient</a> | "
        "<a href='/add-doctor/'>Add Doctor</a> | "
        "<a href='/appointment/'>Book Appointment</a> | "
        "<a href='/report/'>Generate Report</a>"
    )

def add_patient(request):
    return HttpResponse(
        "<h2>🧑‍⚕️ Register Patient</h2>"
        "<form>"
        "Name: <input type='text'><br>"
        "Age: <input type='number'><br>"
        "Gender: <input type='text'><br>"
        "Contact: <input type='text'><br>"
        "<button type='submit'>Add Patient</button>"
        "</form>"
    )

def add_doctor(request):
    return HttpResponse(
        "<h2>👨‍⚕️ Register Doctor</h2>"
        "<form>"
        "Name: <input type='text'><br>"
        "Specialization: <input type='text'><br>"
        "Contact: <input type='text'><br>"
        "<button type='submit'>Add Doctor</button>"
        "</form>"
    )

def appointment(request):
    return HttpResponse(
        "<h2>📅 Book Appointment</h2>"
        "<form>"
        "Patient ID: <input type='text'><br>"
        "Doctor ID: <input type='text'><br>"
        "Date: <input type='date'><br>"
        "Status: <input type='text' placeholder='Pending/Confirmed'><br>"
        "<button type='submit'>Book</button>"
        "</form>"
    )

def report(request):
    return HttpResponse(
        "<h2>📋 Generate Report</h2>"
        "<form>"
        "Patient ID: <input type='text'><br>"
        "Diagnosis: <input type='text'><br>"
        "Prescription: <input type='text'><br>"
        "Date: <input type='date'><br>"
        "<button type='submit'>Generate Report</button>"
        "</form>"
    )
