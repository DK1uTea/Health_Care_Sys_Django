import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
import logging

logger = logging.getLogger(__name__)

class ProxyView(APIView):
    """
    API Gateway view that proxies requests to appropriate services
    """
    service = None
    path = ''
    
    def __init__(self, service=None, path='', **kwargs):
        super().__init__(**kwargs)
        if service:
            self.service = service
        if path:
            self.path = path
            
    def dispatch(self, request, *args, **kwargs):
        """Process all types of HTTP requests and proxy them"""
        # Get the service and the path
        service = kwargs.get('service', self.service)
        path = kwargs.get('path', self.path)
        
        if service not in settings.SERVICE_ROUTES:
            return Response({"error": f"Service '{service}' not found"}, status=404)
        
        # Construct the target URL
        route_config = settings.SERVICE_ROUTES[service]
        target_host = route_config['host']
        target_port = route_config['port']
        target_url = f"http://{target_host}:{target_port}/{path}"
        
        # Forward the request headers
        headers = {}
        for header, value in request.META.items():
            # Convert HTTP_HEADER_NAME to Header-Name format
            if header.startswith('HTTP_'):
                header_name = '-'.join(word.capitalize() for word in header[5:].split('_'))
                headers[header_name] = value
        
        # Add important headers
        if 'HTTP_COOKIE' in request.META:
            headers['Cookie'] = request.META['HTTP_COOKIE']
        
        if 'CONTENT_TYPE' in request.META:
            headers['Content-Type'] = request.META['CONTENT_TYPE']
            
        if 'HTTP_AUTHORIZATION' in request.META:
            headers['Authorization'] = request.META['HTTP_AUTHORIZATION']
        
        # Make the request to the target service
        try:
            method = request.method.lower()
            request_func = getattr(requests, method)
            
            # Handle request data based on method
            kwargs = {'headers': headers, 'allow_redirects': False}
            
            if method in ['post', 'put', 'patch']:
                if request.content_type and 'application/json' in request.content_type:
                    kwargs['json'] = request.data
                else:
                    kwargs['data'] = request.POST
                    kwargs['files'] = request.FILES
            elif method == 'get':
                kwargs['params'] = request.GET.dict()
            
            # Make the request
            response = request_func(target_url, **kwargs)
            
            # Create Django response
            django_response = HttpResponse(
                content=response.content,
                status=response.status_code,
                content_type=response.headers.get('Content-Type', '')
            )
            
            # Forward all headers from the service response
            for header, value in response.headers.items():
                if header.lower() not in ['content-encoding', 'transfer-encoding', 'content-length']:
                    django_response[header] = value
                    
            # Return the Django response
            return django_response
                
        except requests.RequestException as e:
            logger.error(f"Error proxying request to {target_url}: {e}")
            return Response(
                {"error": "Service unavailable", "details": str(e)},
                status=503
            )


class UIRedirectView(View):
    service = None
    path = ''
    
    def __init__(self, service=None, path='', **kwargs):
        super().__init__(**kwargs)
        if service:
            self.service = service
        if path:
            self.path = path
            
    def get(self, request, *args, **kwargs):
        service = kwargs.get('service', self.service)
        path = kwargs.get('path', self.path)
        
        # Map services to their container names (not localhost)
        service_names = {
            'auth': 'auth-service',
            'ehr': 'ehr-service',
            'appointment': 'appointment-service',
            'pharmacy': 'pharmacy-service',
            'lab': 'lab-service',
            'billing': 'billing-service',
            'ai': 'ai-service'
        }
        
        # Use internal container ports
        service_ports = {
            'auth': 8000,  # Container port, not host port
            'ehr': 8001,
            'appointment': 8002,
            'pharmacy': 8003,
            'lab': 8004,
            'billing': 8005,
            'ai': 8006
        }
        
        # Redirect to the appropriate service using container name
        if service in service_names:
            service_host = service_names[service]
            service_port = service_ports[service]
            return HttpResponseRedirect(f'http://{service_host}:{service_port}/{path}')
        
        return HttpResponseRedirect('/')