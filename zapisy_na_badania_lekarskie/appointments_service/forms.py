from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Patient, AppointmentDate, Hospital


class CreateUserForm(UserCreationForm):
    pesel = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'pesel', 'username', 'password1', 'password2']


class AppointmentCreateForm(forms.Form):
    hospitals_available = Hospital.objects.filter(rooms_available__gte=0)
    #dates_free = AppointmentDate.objects.filter(is_free=True)
    doctors_available = Doctor.objects.all()

    doctor = forms.ModelChoiceField(queryset=doctors_available)
    #date = forms.ModelChoiceField(queryset=dates_free)
    hospital = forms.ModelChoiceField(queryset=hospitals_available)
    purpose_of_appointment = forms.CharField(widget=forms.TextInput)


class HospitalSelectForm(forms.Form):
    hospitals_available = Hospital.objects.filter(rooms_available__gte=1)
    hospital = forms.ModelChoiceField(queryset=hospitals_available)


class DoctorSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.hospital = kwargs.pop('hospital')
        super(DoctorSelectForm, self).__init__(*args, **kwargs)
        self.fields['doctor'] = forms.ModelChoiceField(queryset=self.hospital.doctors.all())


class AppointmentDateSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.appointments_dates_available = kwargs.pop('appointments_dates_available')
        super(AppointmentDateSelectForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.ModelChoiceField(queryset=self.appointments_dates_available)

    purpose_of_appointment = forms.CharField(widget=forms.TextInput)

