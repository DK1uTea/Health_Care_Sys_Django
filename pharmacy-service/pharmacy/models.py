from django.db import models
import uuid

class Medication(models.Model):
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    description = models.TextField()
    dosage_form = models.CharField(max_length=100)  # e.g., "Tablet", "Capsule", "Syrup"
    strength = models.CharField(max_length=50)      # e.g., "500mg", "50mg/5ml"
    manufacturer = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'medications'

class MedicationInventory(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    quantity_in_stock = models.IntegerField()
    reorder_level = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'medication_inventory'

class PrescriptionFulfillment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('DISPENSED', 'Dispensed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prescription_id = models.UUIDField()  # Reference to EHR service prescription ID
    patient_id = models.UUIDField()  # Reference to patient user_id
    pharmacist_id = models.UUIDField(null=True, blank=True)  # Reference to pharmacist user_id
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    dispense_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prescription_fulfillments'

class MedicationDispensed(models.Model):
    fulfillment = models.ForeignKey(PrescriptionFulfillment, on_delete=models.CASCADE, related_name='medications')
    inventory = models.ForeignKey(MedicationInventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    instructions = models.TextField()
    
    class Meta:
        db_table = 'medications_dispensed'