from django.db import models
from accounts.models import User
from django.utils import timezone
from datetime import datetime, date

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

    def calculate_age(self):
        today = date.today()
        born = self.dob
        # Calculate age based on year difference, then adjust if today's date is before the birthday this year
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    # If you prefer property decorator, making it accessible as an attribute
    @property
    def age(self):
        return self.calculate_age()



class Visit(models.Model):
    patient = models.ForeignKey(Patient, related_name='visits', on_delete=models.CASCADE)  # Removed comma
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)  # Removed comma
    visit_reason = models.TextField()
    diagnosis = models.TextField()
    symptoms = models.TextField()
    cadence = models.TextField()
    visit_date = models.DateTimeField(default=timezone.now)
    