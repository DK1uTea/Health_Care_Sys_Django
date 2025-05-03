from django.db import models
import uuid

class Patient(models.Model):
    user_id = models.UUIDField(unique=True)  # Reference to Auth service User ID
    medical_record_number = models.CharField(max_length=50, unique=True)
    blood_type = models.CharField(max_length=10, blank=True)
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'

class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, related_name='medical_records', on_delete=models.CASCADE)
    created_by = models.UUIDField()  # Reference to Auth service User ID (doctor/nurse)
    record_type = models.CharField(max_length=50)  # e.g., "Visit", "Diagnosis", "Treatment"
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medical_records'

class Diagnosis(models.Model):
    record = models.ForeignKey(MedicalRecord, related_name='diagnoses', on_delete=models.CASCADE)
    diagnosis_code = models.CharField(max_length=20)  # ICD-10 code
    diagnosis_name = models.CharField(max_length=255)
    diagnosis_details = models.TextField()
    diagnosed_by = models.UUIDField()  # Doctor ID
    diagnosed_date = models.DateTimeField()
    
    class Meta:
        db_table = 'diagnoses'

class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, related_name='prescriptions', on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    prescribed_by = models.UUIDField()  # Doctor ID
    prescribed_date = models.DateTimeField()
    
    class Meta:
        db_table = 'prescriptions'