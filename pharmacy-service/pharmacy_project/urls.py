"""
URL configuration for pharmacy_project project.

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
from pharmacy.views import (prescription_list, prescription_detail, 
                           verify_prescription, dispense_prescription,
                           add_medication, update_inventory)

router = DefaultRouter()
# Register your API viewsets here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Template views - changed <int:id> to <uuid:id>
    path('prescriptions/', prescription_list, name='prescription_list'),
    path('prescriptions/<uuid:id>/', prescription_detail, name='prescription_detail'),
    path('prescriptions/<uuid:id>/verify/', verify_prescription, name='verify_prescription'),
    path('prescriptions/<uuid:id>/dispense/', dispense_prescription, name='dispense_prescription'),
    path('medications/add/', add_medication, name='add_medication'),
    path('inventory/<int:id>/update/', update_inventory, name='update_inventory'),
    path('', lambda request: redirect('prescription_list')),  # Redirect to prescription list
]
