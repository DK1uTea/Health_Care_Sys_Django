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
    
    # Root path
    path('', ProxyView.as_view(service='auth', path='login/'), name='home'),
]