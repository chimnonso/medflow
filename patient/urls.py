from django.urls import path
from .views import PatientCreate, PatientDetail, PatientUpdate, PatientDelete, PatientList, VisitCreateView, VisitUpdateView

app_name = "patient"

urlpatterns = [
    path('', PatientList.as_view(), name='patient_list'),
    path('add/', PatientCreate.as_view(), name='patient_add'),
    path('<int:pk>/', PatientDetail.as_view(), name='patient_detail'),
    path('<int:pk>/update/', PatientUpdate.as_view(), name='patient_update'),
    path('<int:pk>/delete/', PatientDelete.as_view(), name='patient_delete'),
    path('visit/<int:pk>/visit/add/', VisitCreateView.as_view(), name='add_visit'),
    path('visit/<int:pk>/update/', VisitUpdateView.as_view(), name='visit_update'),
    # Add other URLs for your app
]
