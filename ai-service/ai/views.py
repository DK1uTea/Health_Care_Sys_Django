from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import DiagnosticAssistant, HealthChatbot
from .models import ChatSession, ChatMessage
from django.http import JsonResponse
import uuid

def diagnostic_assistant(request):
    """Render the diagnostic assistant page"""
    # Add mock patients for the dropdown
    mock_patients = [
        {'id': 1, 'full_name': 'John Doe'},
        {'id': 2, 'full_name': 'Jane Smith'},
        {'id': 3, 'full_name': 'Robert Johnson'},
        {'id': 4, 'full_name': 'Emily Williams'}
    ]
    
    # Common symptoms for the symptom selector
    common_symptoms = [
        "Fever", "Cough", "Headache", "Fatigue", "Sore throat", 
        "Shortness of breath", "Muscle pain", "Nausea", "Vomiting",
        "Diarrhea", "Loss of taste", "Loss of smell", "Chills",
        "Joint pain", "Chest pain", "Abdominal pain", "Dizziness",
        "Runny nose", "Congestion", "Rash"
    ]
    
    return render(request, 'ai/diagnostic_assistant.html', {
        'patients': mock_patients,
        'common_symptoms': common_symptoms
    })

class DiagnosisAPI(APIView):
    """API for diagnostic assistant"""
    
    def post(self, request):
        assistant = DiagnosticAssistant()
        result = assistant.diagnose(request.data.get('symptoms', {}))
        return Response(result)

def health_chatbot(request):
    """Render the chatbot UI"""
    return render(request, 'ai/health_chatbot.html', {
        'title': 'Healthcare Chatbot'
    })

class ChatbotAPI(APIView):
    """API endpoint for chatbot interactions"""
    
    def post(self, request):
        chatbot = HealthChatbot()
        
        if 'symptoms' in request.data:
            # Process symptoms
            diagnosis = chatbot.get_diagnosis(request.data.get('symptoms', {}))
            
            response_text = f"Based on your symptoms, you may have {diagnosis['diagnosis']}.\n"
            response_text += f"Recommended test: {diagnosis['test']}\n"
            response_text += f"Recommended medicine: {diagnosis['medicine']}"
            
            return Response({
                'message': response_text,
                'diagnosis': diagnosis,
            })
        else:
            # Simple response for text messages
            message = request.data.get('message', '')
            response_text = "I'm your healthcare assistant. Please check your symptoms using the symptom checker."
            
            return Response({
                'message': response_text
            })