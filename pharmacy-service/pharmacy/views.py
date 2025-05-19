from django.shortcuts import render, get_object_or_404, redirect
from .models import PrescriptionFulfillment, Medication, MedicationInventory
from datetime import datetime, timedelta
import uuid

def prescription_list(request):
    # Get user type from query param (in a real app, get from request.user)
    user_type = request.GET.get('user_type', 'PHARMACIST')
    
    # Mock prescription data
    prescriptions = [
        {
            'id': uuid.uuid4(),
            'created_at': datetime.now() - timedelta(days=2),
            'patient_name': 'John Doe',
            'patient_id': uuid.uuid4(),
            'status': 'PENDING',
            'medications': [
                {'medication_name': 'Amoxicillin', 'quantity': '30 tablets'},
                {'medication_name': 'Ibuprofen', 'quantity': '20 tablets'}
            ],
            'get_status_display': 'Pending'
        },
        {
            'id': uuid.uuid4(),
            'created_at': datetime.now() - timedelta(days=5),
            'patient_name': 'Jane Smith',
            'patient_id': uuid.uuid4(),
            'status': 'VERIFIED',
            'medications': [
                {'medication_name': 'Lisinopril', 'quantity': '90 tablets'},
            ],
            'get_status_display': 'Verified'
        },
        {
            'id': uuid.uuid4(),
            'created_at': datetime.now() - timedelta(days=10),
            'patient_name': 'Robert Johnson',
            'patient_id': uuid.uuid4(),
            'status': 'DISPENSED',
            'medications': [
                {'medication_name': 'Metformin', 'quantity': '60 tablets'},
                {'medication_name': 'Atorvastatin', 'quantity': '30 tablets'}
            ],
            'get_status_display': 'Dispensed'
        }
    ]
    
    # Mock inventory data
    inventory_items = []
    if user_type == 'PHARMACIST':
        inventory_items = [
            {
                'id': 1,
                'medication': {'name': 'Amoxicillin', 'strength': '500mg'},
                'batch_number': 'A12345',
                'expiry_date': datetime.now() + timedelta(days=365),
                'quantity_in_stock': 150,
                'reorder_level': 30
            },
            {
                'id': 2,
                'medication': {'name': 'Ibuprofen', 'strength': '200mg'},
                'batch_number': 'I78901',
                'expiry_date': datetime.now() + timedelta(days=730),
                'quantity_in_stock': 20,
                'reorder_level': 50
            },
            {
                'id': 3,
                'medication': {'name': 'Lisinopril', 'strength': '10mg'},
                'batch_number': 'L45678',
                'expiry_date': datetime.now() + timedelta(days=545),
                'quantity_in_stock': 75,
                'reorder_level': 25
            },
            {
                'id': 4,
                'medication': {'name': 'Metformin', 'strength': '500mg'},
                'batch_number': 'M98765',
                'expiry_date': datetime.now() + timedelta(days=300),
                'quantity_in_stock': 5,
                'reorder_level': 20
            }
        ]
    
    context = {
        'prescriptions': prescriptions,
        'inventory_items': inventory_items,
        'user': {'user_type': user_type}
    }
    
    return render(request, 'pharmacy/prescription_list.html', context)

def prescription_detail(request, id):
    # Get actual prescription or mock data
    prescription = {
        'id': id,
        'created_at': datetime.now() - timedelta(days=2),
        'patient_name': 'John Doe',
        'patient_id': uuid.uuid4(),
        'doctor_name': 'Dr. Sarah Miller',
        'status': 'PENDING',
        'medications': [
            {'medication_name': 'Amoxicillin', 'quantity': '30 tablets', 'instructions': 'Take one tablet three times daily with food'},
            {'medication_name': 'Ibuprofen', 'quantity': '20 tablets', 'instructions': 'Take one tablet as needed for pain, not to exceed 4 in 24 hours'}
        ],
        'notes': 'Patient has history of allergies to penicillin.',
        'get_status_display': 'Pending'
    }
    
    return render(request, 'pharmacy/prescription_detail.html', {'prescription': prescription})

def verify_prescription(request, id):
    # Logic to verify prescription
    return redirect('prescription_list')

def dispense_prescription(request, id):
    # Logic to dispense prescription
    return redirect('prescription_list')

def add_medication(request):
    # Logic to add medication
    return render(request, 'pharmacy/add_medication.html')

def update_inventory(request, id):
    # Logic to update inventory
    return render(request, 'pharmacy/update_inventory.html')
