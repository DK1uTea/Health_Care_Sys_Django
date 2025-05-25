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
    """API endpoint for the health chatbot"""
    
    def post(self, request):
        message = request.data.get('message', '')
        symptoms = request.data.get('symptoms', None)
        session_id = request.session.session_key
        
        chatbot = HealthChatbot()
        
        if not session_id:
            request.session.save()
            session_id = request.session.session_key
        
        if symptoms:
            # Handle symptom checker form submission
            result = self._analyze_symptom_form(chatbot, symptoms)
            return Response(result)
        else:
            # Handle conversational messages
            result = chatbot.process_message(message, session_id)
            return Response(result)
    
    def _analyze_symptom_form(self, chatbot, symptoms):
        """Process structured symptom data from the form"""
        # Calculate which symptoms are present (value = 1)
        present_symptoms = [s for s, v in symptoms.items() if v == 1]
        
        if not present_symptoms:
            return {
                "message": "You haven't selected any symptoms. It seems you're feeling well!",
            }
        
        # Create symptom dictionary in required format
        symptom_dict = {s: 1 if s in present_symptoms else 0 for s in chatbot.symptom_names}
        
        # Get diagnosis
        diagnosis = chatbot._make_diagnosis(symptom_dict)
        
        # Construct response
        response_message = f"Based on your symptoms, you might have {diagnosis['diagnosis']}. "
        response_message += f"I recommend getting a {diagnosis['test']} to confirm this. "
        response_message += f"Typical treatment includes {diagnosis['medicine']}."
        
        return {
            "message": response_message,
            "diagnosis": diagnosis
        }