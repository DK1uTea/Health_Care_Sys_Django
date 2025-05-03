from django.shortcuts import render, get_object_or_404, redirect

def invoice(request, bill_id):
    # Mock data - replace with actual queries
    bill = {
        'id': bill_id,
        'generated_date': '2023-07-10',
        'due_date': '2023-08-10',
        'total_amount': 500,
        'tax': 45,
        'discount': 25,
        'final_amount': 520,
        'status': 'UNPAID',
        'items': [],
        'payments': []
    }
    
    patient = {
        'first_name': 'John',
        'last_name': 'Doe',
        'address': '123 Main St\nAnytown, USA',
        'email': 'john@example.com',
        'phone_number': '555-123-4567'
    }
    
    context = {
        'bill': bill,
        'patient': patient,
        'tax_percent': 9,
        'amount_paid': 0,
        'balance_due': 520,
        'user': {'user_type': 'PATIENT'}
    }
    
    return render(request, 'billing/invoice.html', context)

def patient_bills(request):
    # Show list of bills
    return render(request, 'billing/patient_bills.html', {'bills': [], 'user': {'user_type': 'PATIENT'}})

def make_payment(request, bill_id):
    # Process payment
    return redirect('invoice', bill_id=bill_id)

def download_invoice_pdf(request, bill_id):
    # Generate PDF
    return redirect('invoice', bill_id=bill_id)

def edit_bill(request, bill_id):
    # Show bill editing form
    return render(request, 'billing/edit_bill.html', {'bill_id': bill_id})
