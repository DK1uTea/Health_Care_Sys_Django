from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

def diagnostic_assistant(request):
    # Mock data - replace with real data in production
    patients = [
        {'id': 1, 'full_name': 'John Doe'},
        {'id': 2, 'full_name': 'Jane Smith'}
    ]
    
    return render(request, 'ai/diagnostic_assistant.html', {'patients': patients})

class DiagnosisAPI(APIView):
    def post(self, request):
        # Process AI diagnosis logic
        # This would call your actual ML model
        
        # Mock response
        diagnoses = [
            {
                "icd_code": "J06.9",
                "name": "Acute upper respiratory infection",
                "confidence": 0.82
            },
            {
                "icd_code": "J02.9",
                "name": "Acute pharyngitis",
                "confidence": 0.67
            },
            {
                "icd_code": "J01.9",
                "name": "Acute sinusitis",
                "confidence": 0.45
            }
        ]
        
        return Response({'diagnoses': diagnoses})