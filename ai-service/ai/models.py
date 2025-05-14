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

class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(null=True, blank=True)  # Optional user reference
    session_key = models.CharField(max_length=64, unique=True)  # For anonymous sessions
    created_at = models.DateTimeField(auto_now_add=True)
    last_interaction = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_sessions'

class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_bot = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    symptoms = models.JSONField(null=True, blank=True)
    diagnosis = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']