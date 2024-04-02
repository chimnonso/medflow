from django.db import models
from accounts.models import User
from django.utils import timezone

SEX = [
    ('M', 'Male'),
    ('F', 'Female'),
]

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    Sex = models.CharField(max_length=2, choices=SEX)
    address = models.TextField()
    dob = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Visit(models.Model):
    patient = models.ForeignKey(Patient, related_name='visits', on_delete=models.CASCADE)  # Removed comma
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)  # Removed comma
    visit_reason = models.TextField()
    diagnosis = models.TextField()
    symptoms = models.TextField()
    cadence = models.TextField()
    visit_date = models.DateTimeField(default=timezone.now)
    