from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Patient, Visit, Inventory, Prescription
from .forms import PatientForm, VisitForm, InventoryForm, PrescriptionForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.core.exceptions import ValidationError


class PatientList(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Patient
    template_name = 'patient/patient_list.html'  # Specify your template name
    context_object_name = 'patients'  # Optional: to refer to the object list as 'patients' in your template


class PatientCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'accounts:login'
    model = Patient
    form_class = PatientForm
    template_name = 'patient/patient_form.html'
    success_url = reverse_lazy('patient:patient_list')  # Replace 'patient_list' with your actual URL name for listing patients
    success_message =  "%(first_name)s added successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user as created_by
        return super().form_valid(form)

class PatientDetail(LoginRequiredMixin, DetailView):
    login_url = 'accounts:login'
    model = Patient
    template_name = 'patient/patient_detail.html'

class PatientUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'accounts:login'
    model = Patient
    form_class = PatientForm
    template_name = 'patient/patient_form.html'
    success_url = reverse_lazy('patient:patient_list')  # Replace 'patient_list' with your actual URL name
    success_message =  "Patient updated successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user as created_by
        return super().form_valid(form)

class PatientDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'accounts:login'
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patient:patient_list')  # Replace 'patient_list' with your actual URL name
    success_message =  "Patient deleted successfully"


class VisitCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    model = Visit
    form_class = VisitForm
    template_name = 'patient/visit_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # Get the patient ID from the URL
        patient_id = self.kwargs.get('pk')
        initial['patient'] = Patient.objects.get(pk=patient_id)
        return initial

    def form_valid(self, form):
        form.instance.patient_id = self.kwargs.get('pk')  # Set the patient based on the URL
        form.instance.doctor = self.request.user
        # Add success message
        messages.success(self.request, 'Visit created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        patient_id = self.kwargs.get('pk')
        return reverse_lazy('patient:patient_detail', kwargs={'pk': patient_id})  # Adjust this to your needs


class VisitUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    model = Visit
    form_class = VisitForm
    template_name = 'patient/visit_form.html'

    def form_valid(self, form):
        form.instance.patient_id = self.kwargs.get('pk')
        form.instance.doctor = self.request.user
        response = super().form_valid(form)
        # Add success message
        messages.success(self.request, 'Visit updated successfully!')
        return response

    def get_success_url(self):
        patient_id = self.kwargs.get('pk')
        return reverse_lazy('patient:patient_detail', kwargs={'pk': patient_id})

class InventoryList(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Inventory
    context_object_name = 'inventory'
    template_name = 'inventory/inventory_list.html'

class InventoryDetail(LoginRequiredMixin, DetailView):
    login_url = 'accounts:login'
    model = Inventory
    context_object_name = 'item'
    template_name = 'inventory/inventory_detail.html'

class InventoryCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'accounts:login'
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('patient:inventory-list')
    success_message =  "Inventory created successfully"

class InventoryUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'accounts:login'
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('patient:inventory-list')
    success_message =  "Inventory updated successfully"

class InventoryDelete(LoginRequiredMixin, DeleteView):
    login_url = 'accounts:login'
    model = Inventory
    context_object_name = 'item'
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('patient:inventory-list')


class PrescriptionList(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Prescription
    context_object_name = 'prescriptions'
    template_name = 'prescriptions/prescription_list.html'

class PrescriptionDetail(LoginRequiredMixin, DetailView):
    login_url = 'accounts:login'
    model = Prescription
    context_object_name = 'prescription'
    template_name = 'prescriptions/prescription_detail.html'

class PrescriptionCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'accounts:login'
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescriptions/prescription_form.html'
    success_url = reverse_lazy('patient:prescription-list')
    success_message =  "Prescription created successfully"

class PrescriptionUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescriptions/prescription_form.html'
    success_url = reverse_lazy('patient:patient_list')

    def form_valid(self, form):
        # Get the current instance to compare the old value of `is_filled`
        prescription = form.save(commit=False)
        if 'is_filled' in form.changed_data and form.cleaned_data['is_filled']:
            # If `is_filled` has been changed to True, update inventory
            inventory_item = prescription.medicine
            try:
                # Attempt to convert dosage and frequency to integers
                dosage = int(prescription.dosage)
                frequency = int(prescription.frequency)
                duration = int(prescription.duration)
                amount_to_reduce = dosage * frequency * duration

                if inventory_item and inventory_item.quantity_in_stock >= amount_to_reduce:
                    # Reduce the stock count safely using F()
                    inventory_item.quantity_in_stock = F('quantity_in_stock') - amount_to_reduce
                    inventory_item.save()
                    messages.success(self.request, 'Prescription updated successfully!')
                    inventory_item.refresh_from_db()  # To get the updated stock value if needed elsewhere
                else:
                    # Raise an error if stock is insufficient
                    form.add_error(None, 'Insufficient stock to fulfill prescription.')
                    return self.form_invalid(form)
            except ValueError:
                # Handle the case where conversion to integer fails
                form.add_error('dosage', 'Dosage and frequency must be numeric.')
                form.add_error('frequency', 'Dosage and frequency must be numeric.')
                return self.form_invalid(form)

        # Save the changes to the prescription
        prescription.save()
        return super(PrescriptionUpdate, self).form_valid(form)

class PrescriptionDelete(LoginRequiredMixin, DeleteView):
    login_url = 'accounts:login'
    model = Prescription
    context_object_name = 'prescription'
    template_name = 'prescriptions/prescription_confirm_delete.html'
    success_url = reverse_lazy('patient:prescription-list')