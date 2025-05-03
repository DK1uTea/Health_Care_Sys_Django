from django.db import models
import uuid

class AIModel(models.Model):
    MODEL_TYPES = (
        ('DIAGNOSTIC', 'Diagnostic Assistant'),
        ('PREDICTIVE', 'Predictive Analytics'),
        ('NLP', 'Natural Language Processing'),
        ('IMAGE', 'Medical Imaging Analysis'),
    )
    
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    active = models.BooleanField(default=True)
    description = models.TextField()
    model_file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_models'
        unique_together = ('name', 'version')

class DiagnosticSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_id = models.UUIDField()  # Reference to doctor user_id
    patient_id = models.UUIDField()  # Reference to patient user_id
    medical_record_id = models.UUIDField()  # Reference to EHR service record ID
    model = models.ForeignKey(AIModel, on_delete=models.PROTECT)
    symptoms = models.JSONField()
    diagnosis_result = models.JSONField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'diagnostic_sessions'