from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


def only_numbers(value: str):
    for number in value:
        if not number.isdigit():
            raise ValidationError('Pesel musi składać sie z samych cyfr')


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    country_identifier = models.CharField(max_length=3)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=6)
    rooms_available = models.IntegerField(default=5)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pesel = models.CharField(max_length=11, validators=[only_numbers])
    login = models.CharField(max_length=20)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.SET_NULL, related_name='doctors', default=None)
    specialization = models.TextField()

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name) + ', specjalizacja: ' + str(self.specialization)


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pesel = models.CharField(max_length=11, validators=[only_numbers])
    login = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class AppointmentDate(models.Model):
    date = models.DateTimeField(default=None, blank=True, null=True, unique=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date}'


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL,null=True,blank=True, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    date = models.ForeignKey(AppointmentDate, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    purpose_of_appointment = models.TextField(max_length=250)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if len(str(self.purpose_of_appointment)) <= 20:
            return self.purpose_of_appointment

        return str(self.purpose_of_appointment)[:20] + '...'


class AppointmentHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_history')
    diagnosis = models.TextField()

    def __str__(self):
        return str(self.diagnosis)[:10] + '...'