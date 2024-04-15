from django.urls import path
from .views import PatientCreate, PatientDetail, PatientUpdate, PatientDelete, PatientList, VisitCreateView, VisitUpdateView, InventoryList, InventoryDetail, InventoryDelete, InventoryCreate, InventoryUpdate, PrescriptionList, PrescriptionDetail, PrescriptionCreate, PrescriptionUpdate, PrescriptionDelete

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

    path('inventory/', InventoryList.as_view(), name='inventory-list'),
    path('inventory/<int:pk>/', InventoryDetail.as_view(), name='inventory-detail'),
    path('inventory/add/', InventoryCreate.as_view(), name='inventory-add'),
    path('inventory/<int:pk>/update/', InventoryUpdate.as_view(), name='inventory-update'),
    path('inventory/<int:pk>/delete/', InventoryDelete.as_view(), name='inventory-delete'),

    path('prescriptions/', PrescriptionList.as_view(), name='prescription-list'),
    path('prescriptions/<int:pk>/', PrescriptionDetail.as_view(), name='prescription-detail'),
    path('prescriptions/add/', PrescriptionCreate.as_view(), name='prescription-add'),
    path('prescriptions/<int:pk>/update/', PrescriptionUpdate.as_view(), name='prescription-update'),
    path('prescriptions/<int:pk>/delete/', PrescriptionDelete.as_view(), name='prescription-delete'),
]
