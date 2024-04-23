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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
    visit_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.visit_date}"
    

class Inventory(models.Model):
    medicine_name = models.CharField(max_length=100)
    quantity_in_stock = models.IntegerField()
    expiry_date = models.DateField()
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicine_name} - {self.quantity_in_stock} units"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    visit = models.ForeignKey('Visit', on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, related_name='prescriptions')
    dosage = models.IntegerField()
    frequency = models.IntegerField()
    duration = models.IntegerField("Number of weeks")
    prescribed_date = models.DateField(default=date.today)
    is_filled = models.BooleanField(default=False)

    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.last_name} on {self.prescribed_date}"
