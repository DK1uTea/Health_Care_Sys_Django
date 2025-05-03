from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from appointments.views import DoctorViewSet, ScheduleViewSet, AppointmentViewSet
from appointments.views import appointment_list, appointment_detail

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Template routes
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/<int:id>/', appointment_detail, name='appointment_detail'),
    path('appointments/book/', appointment_list, name='book_appointment'),
    path('appointments/<int:id>/cancel/', appointment_detail, name='cancel_appointment'),
    path('', lambda request: redirect('appointment_list')),  # Redirect to appointment list
]