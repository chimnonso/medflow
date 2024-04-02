from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = [
    ('PH', 'Pharmacist'),
    ('TN', 'Pharmacy Technician'),
    ('AD', 'Administrator'),
    ('DR', 'Doctor'),
    # ('PA', 'Patient'),
]

class User(AbstractUser):
    role = models.CharField(max_length=2, choices=ROLES)