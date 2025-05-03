from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, MedicalRecord, Diagnosis, Prescription
from .serializers import PatientSerializer, MedicalRecordSerializer, DiagnosisSerializer, PrescriptionSerializer
import requests

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    
    def get_queryset(self):
        return MedicalRecord.objects.all()
    
    @action(detail=True, methods=['post'])
    def ai_diagnosis(self, request, pk=None):
        """Use AI to suggest diagnoses based on symptoms"""
        record = self.get_object()
        symptoms = request.data.get('symptoms', [])
        
        # Sample AI service call (mocked for simplicity)
        # In a real implementation, this would call the AI microservice
        ai_diagnosis = {
            "diagnoses": [
                {
                    "icd_code": "J06.9",
                    "name": "Acute upper respiratory infection",
                    "confidence": 0.82,
                    "suggested_by_ai": True
                }
            ]
        }
        
        return Response({
            "record_id": str(record.id),
            "ai_suggestions": ai_diagnosis['diagnoses']
        })

def patient_records(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
    
    context = {
        'patient': patient,
        'medical_records': medical_records
    }
    return render(request, 'records/patient_records.html', context)

def record_detail(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    context = {
        'record': record
    }
    return render(request, 'records/record_detail.html', context)

def add_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        # Process form data
        # ...
        return redirect('patient_records', patient_id=patient.id)
    
    context = {
        'patient': patient
    }
    return render(request, 'records/add_record.html', context)