"""
URL configuration for billing_project project.

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
# Import your views here (create these in billing/views.py if they don't exist)
from billing.views import invoice, patient_bills, make_payment, download_invoice_pdf, edit_bill

router = DefaultRouter()
# Register your API viewsets here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Template views
    path('bills/<int:bill_id>/', invoice, name='invoice'),
    path('bills/', patient_bills, name='patient_bills'),
    path('bills/<int:bill_id>/payment/', make_payment, name='make_payment'),
    path('bills/<int:bill_id>/pdf/', download_invoice_pdf, name='download_invoice_pdf'),
    path('bills/<int:bill_id>/edit/', edit_bill, name='edit_bill'),
    path('', lambda request: redirect('patient_bills')),  # Redirect to bills list
]
