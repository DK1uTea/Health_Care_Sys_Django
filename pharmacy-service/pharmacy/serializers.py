from rest_framework import serializers
from .models import Medication, MedicationInventory, PrescriptionFulfillment, MedicationDispensed

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class MedicationInventorySerializer(serializers.ModelSerializer):
    medication_name = serializers.ReadOnlyField(source='medication.name')
    
    class Meta:
        model = MedicationInventory
        fields = '__all__'

class MedicationDispensedSerializer(serializers.ModelSerializer):
    medication_name = serializers.ReadOnlyField(source='inventory.medication.name')
    
    class Meta:
        model = MedicationDispensed
        fields = '__all__'

class PrescriptionFulfillmentSerializer(serializers.ModelSerializer):
    medications = MedicationDispensedSerializer(many=True, read_only=True)
    
    class Meta:
        model = PrescriptionFulfillment
        fields = '__all__'