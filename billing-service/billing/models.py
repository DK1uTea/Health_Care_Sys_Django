from django.db import models
import uuid

class InsuranceProvider(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    class Meta:
        db_table = 'insurance_providers'

class PatientInsurance(models.Model):
    patient_id = models.UUIDField()  # Reference to patient user_id
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100)
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'patient_insurances'

class ServiceItem(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.CharField(max_length=50)  # e.g., "Consultation", "Procedure", "Lab"
    
    class Meta:
        db_table = 'service_items'

class Bill(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Payment'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.UUIDField()  # Reference to patient user_id
    related_appointment_id = models.UUIDField(null=True, blank=True)  # Optional reference to appointment
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    generated_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'bills'

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'bill_items'

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('INSURANCE', 'Insurance'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_PAYMENT', 'Mobile Payment'),
    )
    
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_reference = models.CharField(max_length=100, blank=True)
    received_by = models.UUIDField(null=True, blank=True)  # Reference to staff user_id
    
    class Meta:
        db_table = 'payments'