from django.contrib import admin
from django.urls import path, re_path
from proxy.views import ProxyView, UIRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes
    re_path(r'^api/(?P<service>auth|ehr|appointment|pharmacy|lab|billing|ai)/(?P<path>.*)$', 
            ProxyView.as_view(), name='api_gateway'),
    
    # UI routes - proxy instead of redirect
    re_path(r'^(?P<service>auth|ehr|appointment|pharmacy|lab|billing|ai)/(?P<path>.*)$',
            ProxyView.as_view(), name='ui_gateway'),
    
    # Direct auth routes (these need to work without the /auth/ prefix)
    path('login/', ProxyView.as_view(service='auth', path='login/'), name='login'),
    path('register/', ProxyView.as_view(service='auth', path='register/'), name='register'),
    path('dashboard/', ProxyView.as_view(service='auth', path='dashboard/'), name='dashboard'),
    path('logout/', ProxyView.as_view(service='auth', path='logout/'), name='logout'),
    
    # AI direct routes 
    path('ai/', ProxyView.as_view(service='ai', path=''), name='ai_home'),
    path('ai/diagnostic-assistant/', ProxyView.as_view(service='ai', path='diagnostic-assistant/'), name='diagnostic_assistant'),
    path('ai/health-chatbot/', ProxyView.as_view(service='ai', path='health-chatbot/'), name='health_chatbot'),
    
    # Direct API routes for backward compatibility with JavaScript
    path('api/chatbot/', ProxyView.as_view(service='ai', path='chatbot/'), name='api_chatbot'),
    path('api/diagnosis/', ProxyView.as_view(service='ai', path='diagnosis/'), name='api_diagnosis'),
    path('api/patients/', ProxyView.as_view(service='ehr', path='patients/'), name='api_patients'),
    path('api/appointments/', ProxyView.as_view(service='appointment', path='appointments/'), name='api_appointments'),
    path('api/prescriptions/', ProxyView.as_view(service='pharmacy', path='prescriptions/'), name='api_prescriptions'),
    
    # Root path
    path('', ProxyView.as_view(service='auth', path='login/'), name='home'),
]