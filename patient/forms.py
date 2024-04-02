from django import forms
from .models import Patient, Visit

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
        fields = ['visit_reason', 'diagnosis', 'symptoms', 'cadence', 'visit_date']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'})
        }
