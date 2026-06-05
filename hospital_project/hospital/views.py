from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from datetime import date
import json

from .models import User, Patient, Doctor, Appointment, Report, Notification
from .forms import (PatientRegistrationForm, DoctorRegistrationForm,
    AppointmentForm, AppointmentStatusForm, ReportForm,
    PatientSearchForm, DoctorSearchForm)
from .decorators import role_required

def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin': return redirect('admin_dashboard')
        if request.user.role == 'doctor': return redirect('doctor_dashboard')
        return redirect('patient_dashboard')
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_patient(request):
    form = PatientRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('patient_dashboard')
    return render(request, 'auth/register_patient.html', {'form': form})

def register_doctor(request):
    form = DoctorRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Doctor registered! Please log in.')
        return redirect('login')
    return render(request, 'auth/register_doctor.html', {'form': form})

# ── Patient ──────────────────────────────────────
@login_required
@role_required('patient')
def patient_dashboard(request):
    patient = request.user.patient_profile
    ctx = {
        'patient': patient,
        'upcoming_appointments': Appointment.objects.filter(patient=patient, status='scheduled', date__gte=date.today()).select_related('doctor')[:5],
        'recent_reports': Report.objects.filter(patient=patient)[:3],
        'total_appointments': Appointment.objects.filter(patient=patient).count(),
        'completed_appointments': Appointment.objects.filter(patient=patient, status='completed').count(),
    }
    return render(request, 'patient/dashboard.html', ctx)

@login_required
@role_required('patient')
def book_appointment(request):
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appt = form.save(commit=False)
        appt.patient = request.user.patient_profile
        appt.save()
        Notification.objects.create(user=request.user, message=f'Appointment booked with Dr. {appt.doctor.name} on {appt.date}.')
        messages.success(request, 'Appointment booked!')
        return redirect('patient_appointments')
    return render(request, 'patient/book_appointment.html', {'form': form})

@login_required
@role_required('patient')
def patient_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user.patient_profile).select_related('doctor')
    return render(request, 'patient/appointments.html', {'appointments': appointments})

@login_required
@role_required('patient')
def cancel_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, patient=request.user.patient_profile)
    if appt.status == 'scheduled':
        appt.status = 'cancelled'
        appt.save()
        messages.success(request, 'Appointment cancelled.')
    return redirect('patient_appointments')

@login_required
@role_required('patient')
def patient_reports(request):
    reports = Report.objects.filter(patient=request.user.patient_profile).select_related('doctor')
    return render(request, 'patient/reports.html', {'reports': reports})

# ── Doctor ───────────────────────────────────────
@login_required
@role_required('doctor')
def doctor_dashboard(request):
    doctor = request.user.doctor_profile
    ctx = {
        'doctor': doctor,
        'today_appointments': Appointment.objects.filter(doctor=doctor, date=date.today(), status='scheduled').select_related('patient'),
        'upcoming_appointments': Appointment.objects.filter(doctor=doctor, status='scheduled', date__gt=date.today()).select_related('patient')[:5],
        'total_patients': Appointment.objects.filter(doctor=doctor).values('patient').distinct().count(),
        'pending_count': Appointment.objects.filter(doctor=doctor, status='scheduled').count(),
    }
    return render(request, 'doctor/dashboard.html', ctx)

@login_required
@role_required('doctor')
def doctor_appointments(request):
    appts = Appointment.objects.filter(doctor=request.user.doctor_profile).select_related('patient')
    status_filter = request.GET.get('status', '')
    if status_filter:
        appts = appts.filter(status=status_filter)
    return render(request, 'doctor/appointments.html', {'appointments': appts, 'status_filter': status_filter})

@login_required
@role_required('doctor')
def update_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, doctor=request.user.doctor_profile)
    form = AppointmentStatusForm(request.POST or None, instance=appt)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Appointment updated.')
        return redirect('doctor_appointments')
    return render(request, 'doctor/update_appointment.html', {'form': form, 'appointment': appt})

@login_required
@role_required('doctor')
def add_report(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, doctor=request.user.doctor_profile)
    form = ReportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        report = form.save(commit=False)
        report.doctor = request.user.doctor_profile
        report.patient = appt.patient
        report.appointment = appt
        report.save()
        appt.status = 'completed'
        appt.save()
        Notification.objects.create(user=appt.patient.user, message=f'Your report from Dr. {request.user.doctor_profile.name} is ready.')
        messages.success(request, 'Report added!')
        return redirect('doctor_appointments')
    return render(request, 'doctor/add_report.html', {'form': form, 'appointment': appt})

@login_required
@role_required('doctor')
def doctor_patients(request):
    ids = Appointment.objects.filter(doctor=request.user.doctor_profile).values_list('patient_id', flat=True).distinct()
    patients = Patient.objects.filter(id__in=ids)
    return render(request, 'doctor/patients.html', {'patients': patients})

# ── Admin ─────────────────────────────────────────
@login_required
@role_required('admin')
def admin_dashboard(request):
    from django.db.models import Count
    from datetime import timedelta
    today = date.today()
    labels, data = [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%b %d'))
        data.append(Appointment.objects.filter(date=day).count())
    ctx = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='scheduled').count(),
        'recent_appointments': Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:10],
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    return render(request, 'admin/dashboard.html', ctx)

@login_required
@role_required('admin')
def manage_patients(request):
    form = PatientSearchForm(request.GET or None)
    patients = Patient.objects.all()
    if form.is_valid():
        if form.cleaned_data.get('name'):
            patients = patients.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data.get('disease_type'):
            patients = patients.filter(disease_type=form.cleaned_data['disease_type'])
    return render(request, 'admin/patients.html', {'patients': patients, 'form': form})

@login_required
@role_required('admin')
def manage_doctors(request):
    form = DoctorSearchForm(request.GET or None)
    doctors = Doctor.objects.all()
    if form.is_valid():
        if form.cleaned_data.get('name'):
            doctors = doctors.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data.get('specialization'):
            doctors = doctors.filter(specialization=form.cleaned_data['specialization'])
    return render(request, 'admin/doctors.html', {'doctors': doctors, 'form': form})

@login_required
@role_required('admin')
def manage_appointments(request):
    appts = Appointment.objects.select_related('patient', 'doctor').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        appts = appts.filter(status=status_filter)
    return render(request, 'admin/appointments.html', {'appointments': appts, 'status_filter': status_filter})

@login_required
@role_required('admin')
def delete_patient(request, pk):
    get_object_or_404(Patient, pk=pk).user.delete()
    messages.success(request, 'Patient deleted.')
    return redirect('manage_patients')

@login_required
@role_required('admin')
def delete_doctor(request, pk):
    get_object_or_404(Doctor, pk=pk).user.delete()
    messages.success(request, 'Doctor deleted.')
    return redirect('manage_doctors')

@login_required
@role_required('admin')
def toggle_doctor_availability(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.is_available = not doctor.is_available
    doctor.save()
    return redirect('manage_doctors')

@login_required
@role_required('admin')
def export_reports_excel(request):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status'])
    for a in Appointment.objects.select_related('patient', 'doctor').all():
        ws.append([a.id, a.patient.name, a.doctor.name, str(a.date), str(a.time), a.status])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=appointments.xlsx'
    wb.save(response)
    return response

@login_required
@role_required('admin')
def export_reports_pdf(request):
    reports = Report.objects.select_related('patient', 'doctor').all()
    try:
        from xhtml2pdf import pisa
        from django.template.loader import render_to_string
        html = render_to_string('admin/reports_pdf.html', {'reports': reports})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=reports.pdf'
        pisa.CreatePDF(html, dest=response)
        return response
    except ImportError:
        return HttpResponse('Install xhtml2pdf: pip install xhtml2pdf')

@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))