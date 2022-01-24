import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, AppointmentCreateForm, HospitalSelectForm, DoctorSelectForm, \
    AppointmentDateSelectForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Appointment, AppointmentDate, Hospital
from django.views.generic import FormView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View


def _create_patient(data):
    new_patient = Patient(first_name=data['first_name'],
                          last_name=data['last_name'],
                          pesel=data['pesel'],
                          login=data['username'])
    new_patient.save()


def _create_doctor(data):
    new_doctor = Patient(first_name=data['first_name'],
                         last_name=data['last_name'],
                         pesel=data['pesel'],
                         login=data['username'],
                         hospital=None,
                         specialization=data['specialization'])
    new_doctor.save()


def _create_new_appointment(doctor, patient, hospital, date, purpose_of_appointment):
    Appointment.objects.create(doctor=doctor,
                               patient=patient,
                               hospital=hospital,
                               date=date,
                               purpose_of_appointment=purpose_of_appointment)

    hospital.rooms_available -= 1
    hospital.save()


def registration_page(request):
    if request.user.is_authenticated:
        return redirect('appointments-service:main-menu')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                messages.success(request, 'Account was created for ' + username)

                _create_patient(form.cleaned_data)

                return redirect('appointments-service:login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('appointments-service:main-menu')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('appointments-service:main-menu')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('appointments-service:login')


@login_required(login_url='appointments-service:login')
def main_menu_redirect(request):
    return HttpResponseRedirect(reverse('appointments-service:main-menu'))


@login_required(login_url='appointments-service:login')
def main_menu(request):
    context = {'username': request.user.username}
    return render(
        request,
        'main_menu.html',
        context
    )


class HospitalSelectView(View):
    def get(self, request):
        form = HospitalSelectForm()
        return render(
            request,
            template_name='appointment_creation/hospital_select_view.html',
            context={'form': form}
        )

    def post(self, request):
        form = HospitalSelectForm(request.POST or None)
        if form.is_valid():
            hospital = form.cleaned_data['hospital']

            return redirect('appointments-service:doctor-select-view', pk=hospital.pk)

        return render(
            request,
            template_name='appointment_creation/hospital_select_view.html',
            context={'form': form}
        )


class DoctorSelectView(View):
    def get(self, request, pk):
        hospital = Hospital.objects.get(pk=pk)

        form = DoctorSelectForm(hospital=hospital)
        return render(
            request,
            template_name='appointment_creation/doctor_select_view.html',
            context={'form': form}
        )

    def post(self, request, pk):
        hospital = Hospital.objects.get(pk=pk)
        form = DoctorSelectForm(request.POST or None, hospital=hospital)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']

            # sprawdzenie wolnych terminów dla doktora

            return redirect('appointments-service:appointment-date-select-view', pk=doctor.pk)

        return render(
            request,
            template_name='appointment_creation/doctor_select_view.html',
            context={'form': form}
        )


class AppointmentDateSelectView(View):
    def get(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)

        #sprawdzenie wolnych terminów dla doktora
        doctors_appointments = doctor.appointments.all()
        saved_dates_pks = []
        for app in doctors_appointments:
            saved_dates_pks.append(app.date.pk)

        now = datetime.datetime.now()
        appointments_dates_available = AppointmentDate.objects.filter(date__gte=now) \
            .exclude(pk__in=saved_dates_pks)

        form = AppointmentDateSelectForm(appointments_dates_available=appointments_dates_available)
        return render(
            request,
            template_name='appointment_creation/appointment_date_select_view.html',
            context={'form': form, 'doctor': doctor}
        )

    def post(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)

        # sprawdzenie wolnych terminów dla doktora
        doctors_appointments = doctor.appointments.all()
        saved_dates_pks = []
        for app in doctors_appointments:
            saved_dates_pks.append(app.date.pk)

        now = datetime.datetime.now()
        appointments_dates_available = AppointmentDate.objects.filter(date__gte=now) \
            .exclude(pk__in=saved_dates_pks)

        form = AppointmentDateSelectForm(request.POST or None, appointments_dates_available=appointments_dates_available)
        if form.is_valid():
            date = form.cleaned_data['date']
            purpose_of_appointment = form.cleaned_data['purpose_of_appointment']

            _create_new_appointment(doctor,
                                    Patient.objects.get(login=str(request.user.username)),
                                    doctor.hospital,
                                    date,
                                    purpose_of_appointment)

            messages.success(request, 'Pomyślnie zapisano na wizytę!')
            return redirect('appointments-service:main-menu')

        return render(
            request,
            template_name='appointment_creation/appointment_date_select_view.html',
            context={'form': form}
        )


# class AppointmentCreateView(View):
#     def get(self, request):
#         form = AppointmentCreateForm()
#         return render(
#             request,
#             template_name='appointments_create_view.html',
#             context={'form': form}
#         )
#
#     def post(self, request):
#         form = AppointmentCreateForm(request.POST or None)
#         if form.is_valid():
#             doctor = form.cleaned_data['doctor']
#             patient = Patient.objects.get(login=str(request.user.username))
#             hospital = form.cleaned_data['hospital']
#             date = form.cleaned_data['date']
#             purpose_of_appointment = form.cleaned_data['purpose_of_appointment']
#
#             Appointment.objects.create(doctor=doctor,
#                                        patient=patient,
#                                        hospital=hospital,
#                                        date=date,
#                                        purpose_of_appointment=purpose_of_appointment, )
#
#             # zablokowanie terminu i miejsca w szpitalu
#             p = date
#             p.is_free = False
#             p.save()
#             hospital.rooms_available -= 1
#             hospital.save()
#
#             messages.success(request, "Pomyślnie dodano nową wizytę!")
#
#             return redirect('appointments-service:main-menu')
#         return render(
#             request,
#             template_name='appointments_create_view.html',
#             context={'form': form}
#         )


class AppointmentsListView(View):
    def get(self, request):
        return render(
            request,
            template_name='appointments_list_view.html',
            context={'appointments': Appointment.objects.filter(patient__login=str(request.user.username))}
        )


class AppointmentsDeleteView(View):
    def get(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)

        context = {'appointment': appointment}
        return render(
            request,
            template_name='appointments_delete_view.html',
            context=context
        )

    def post(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        free_date = appointment.date
        free_date.is_free = True
        free_date.save()
        appointment.delete()

        messages.info(request, f'Usunięto twoją wizytę {appointment}')
        return redirect('appointments-service:appointments-list-view')


class AppointmentsDetailView(View):
    def get(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        info = {'Lekarz prowadzący': appointment.doctor,
                'Pacjent': appointment.patient,
                'Szpital': appointment.hospital,
                'Termin': appointment.date,
                'Cel wizyty': appointment.purpose_of_appointment}

        context = {'info': info}
        return render(
            request,
            template_name='appointments_detail_view.html',
            context=context
        )
