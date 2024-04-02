from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Patient, Visit
from .forms import PatientForm, VisitForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

class PatientList(ListView):
    model = Patient
    template_name = 'patient/patient_list.html'  # Specify your template name
    context_object_name = 'patients'  # Optional: to refer to the object list as 'patients' in your template


class PatientCreate(SuccessMessageMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient/patient_form.html'
    success_url = reverse_lazy('patient:patient_list')  # Replace 'patient_list' with your actual URL name for listing patients
    success_message =  "%(first_name)s added successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user as created_by
        return super().form_valid(form)

class PatientDetail(DetailView):
    model = Patient
    template_name = 'patient/patient_detail.html'

class PatientUpdate(SuccessMessageMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient/patient_form.html'
    success_url = reverse_lazy('patient:patient_list')  # Replace 'patient_list' with your actual URL name
    success_message =  "Patient updated successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user as created_by
        return super().form_valid(form)

class PatientDelete(SuccessMessageMixin, DeleteView):
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patient:patient_list')  # Replace 'patient_list' with your actual URL name
    success_message =  "Patient deleted successfully"


class VisitCreateView(CreateView):
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


class VisitUpdateView(UpdateView):
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