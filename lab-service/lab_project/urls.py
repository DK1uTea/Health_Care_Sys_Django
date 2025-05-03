"""
URL configuration for lab_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from lab.views import test_results, enter_test_result, update_test_result, complete_test_order, download_test_report

router = DefaultRouter()
# Register your API viewsets here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Template routes
    path('orders/<int:order_id>/results/', test_results, name='test_results'),
    path('tests/<int:test_id>/enter-result/', enter_test_result, name='enter_test_result'),
    path('results/<int:result_id>/update/', update_test_result, name='update_test_result'),
    path('orders/<int:order_id>/complete/', complete_test_order, name='complete_test_order'),
    path('orders/<int:order_id>/download-report/', download_test_report, name='download_test_report'),
    path('', lambda request: redirect('test_results', order_id=1)),  # Redirect to first order
]
