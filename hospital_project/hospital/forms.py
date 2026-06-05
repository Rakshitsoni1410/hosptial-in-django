from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor, Appointment, Report
from .mixins import BootstrapFormMixin

class PatientRegistrationForm(BootstrapFormMixin, UserCreationForm):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=1)
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES)
    contact = forms.CharField(max_length=15)
    blood_group = forms.CharField(max_length=5, required=False)
    disease_type = forms.ChoiceField(choices=Patient.DISEASE_CHOICES)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                contact=self.cleaned_data['contact'],
                blood_group=self.cleaned_data.get('blood_group'),
                disease_type=self.cleaned_data['disease_type'],
                address=self.cleaned_data.get('address'),
            )
        return user

class DoctorRegistrationForm(BootstrapFormMixin, UserCreationForm):
    name = forms.CharField(max_length=100)
    specialization = forms.ChoiceField(choices=Doctor.SPECIALIZATION_CHOICES)
    contact = forms.CharField(max_length=15)
    qualification = forms.CharField(max_length=100, required=False)
    experience_years = forms.IntegerField(min_value=0, initial=0)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'doctor'
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                specialization=self.cleaned_data['specialization'],
                contact=self.cleaned_data['contact'],
                qualification=self.cleaned_data.get('qualification', ''),
                experience_years=self.cleaned_data.get('experience_years', 0),
            )
        return user

class AppointmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

class AppointmentStatusForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'remarks']
        widgets = {'remarks': forms.Textarea(attrs={'rows': 3})}

class ReportForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Report
        fields = ['diagnosis', 'prescription', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class PatientSearchForm(BootstrapFormMixin, forms.Form):
    name = forms.CharField(required=False)
    disease_type = forms.ChoiceField(required=False, choices=[('', 'All')] + list(Patient.DISEASE_CHOICES))

class DoctorSearchForm(BootstrapFormMixin, forms.Form):
    name = forms.CharField(required=False)
    specialization = forms.ChoiceField(required=False, choices=[('', 'All')] + list(Doctor.SPECIALIZATION_CHOICES))