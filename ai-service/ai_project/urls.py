from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ai.views import diagnostic_assistant, DiagnosisAPI

router = DefaultRouter()
# Register your API viewsets here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/diagnosis/', DiagnosisAPI.as_view(), name='diagnosis_api'),
    
    # Template views
    path('diagnostic-assistant/', diagnostic_assistant, name='diagnostic_assistant'),
    path('', lambda request: redirect('diagnostic_assistant')),  # Redirect to diagnostic assistant
]