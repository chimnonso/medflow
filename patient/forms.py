from django import forms
from .models import Patient, Visit, Inventory, Prescription

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'Sex', 'address', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }



class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['visit_reason', 'diagnosis', 'symptoms', 'visit_date']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'})
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['medicine_name', 'quantity_in_stock', 'expiry_date', 'manufacturer']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medicine', 'dosage', 'frequency', 'duration', 'visit', 'is_filled']
        widgets = {
            'prescribed_date': forms.DateInput(attrs={'type': 'date'})
        }

    
