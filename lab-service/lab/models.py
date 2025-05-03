from django.db import models
import uuid

class LabTest(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_instructions = models.TextField(blank=True)
    turnaround_time_hours = models.IntegerField()
    
    class Meta:
        db_table = 'lab_tests'

class TestOrder(models.Model):
    STATUS_CHOICES = (
        ('ORDERED', 'Ordered'),
        ('SPECIMEN_COLLECTED', 'Specimen Collected'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.UUIDField()  # Reference to patient user_id
    ordered_by = models.UUIDField()  # Reference to doctor user_id
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ORDERED')
    ordered_date = models.DateTimeField()
    medical_record_id = models.UUIDField()  # Reference to EHR service record ID
    priority = models.CharField(max_length=20, default='ROUTINE')  # ROUTINE, STAT, URGENT
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'test_orders'

class OrderedTest(models.Model):
    order = models.ForeignKey(TestOrder, on_delete=models.CASCADE, related_name='ordered_tests')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ordered_tests'
        unique_together = ('order', 'test')

class TestResult(models.Model):
    ordered_test = models.OneToOneField(OrderedTest, on_delete=models.CASCADE, related_name='result')
    performed_by = models.UUIDField()  # Reference to lab technician user_id
    performed_at = models.DateTimeField()
    result_value = models.TextField()
    reference_range = models.CharField(max_length=100, blank=True)
    abnormal = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    report_file = models.FileField(upload_to='lab_reports/', null=True, blank=True)
    
    class Meta:
        db_table = 'test_results'