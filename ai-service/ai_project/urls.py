from django.contrib import admin
from django.urls import path
from ai.views import diagnostic_assistant, DiagnosisAPI, health_chatbot, ChatbotAPI
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('diagnostic-assistant/', diagnostic_assistant, name='diagnostic_assistant'),
    path('health-chatbot/', health_chatbot, name='health_chatbot'),
    path('api/diagnosis/', DiagnosisAPI.as_view(), name='diagnosis_api'),
    path('api/chatbot/', ChatbotAPI.as_view(), name='chatbot_api'),
    path('', lambda request: redirect('health_chatbot')),
]