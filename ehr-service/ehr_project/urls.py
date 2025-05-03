from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from records.views import patient_records, record_detail, add_record

router = DefaultRouter()
# Register your API viewsets here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Template views
    path('patients/<int:patient_id>/records/', patient_records, name='patient_records'),
    path('records/<int:record_id>/', record_detail, name='record_detail'),
    path('patients/<int:patient_id>/records/add/', add_record, name='add_record'),
    path('', lambda request: redirect('patient_records', patient_id=1)),  # Redirect to first patient
]