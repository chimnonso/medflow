from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Patient
import datetime

User = get_user_model()
# Create your tests here.

class PatientCRUDTestCase(TestCase):
    def setUp(self):
        # Create a user for the 'created_by' field
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        
    def test_create_patient(self):
        # Test creating a new Patient instance
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            Sex='Male',
            address='123 Main St',
            dob=datetime.date(1990, 1, 1),
            created_by=self.user
        )
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Patient.objects.first(), patient)

    def test_read_patient(self):
        # Test reading a Patient instance
        patient = Patient.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.com',
            Sex='Female',
            address='456 Main St',
            dob=datetime.date(1991, 2, 2),
            created_by=self.user
        )
        fetched_patient = Patient.objects.get(id=patient.id)
        self.assertEqual(fetched_patient, patient)

    def test_update_patient(self):
        # Test updating a Patient instance
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            Sex='Male',
            address='123 Main St',
            dob=datetime.date(1990, 1, 1),
            created_by=self.user
        )
        patient.first_name = 'Jonathan'
        patient.save()
        updated_patient = Patient.objects.get(id=patient.id)
        self.assertEqual(updated_patient.first_name, 'Jonathan')

    def test_delete_patient(self):
        # Test deleting a Patient instance
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            Sex='Male',
            address='123 Main St',
            dob=datetime.date(1990, 1, 1),
            created_by=self.user
        )
        patient_id = patient.id
        patient.delete()
        with self.assertRaises(Patient.DoesNotExist):
            Patient.objects.get(id=patient_id)
