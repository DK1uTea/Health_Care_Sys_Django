from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Schedule, Appointment
from .serializers import DoctorSerializer, ScheduleSerializer, AppointmentSerializer
from datetime import datetime, timedelta

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        doctor_id = request.query_params.get('doctor')
        date_str = request.query_params.get('date')
        
        if not doctor_id or not date_str:
            return Response({"error": "Doctor ID and date are required"}, status=400)
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (Doctor.DoesNotExist, ValueError):
            return Response({"error": "Invalid doctor ID or date format"}, status=400)
        
        # Get the day of week (0=Monday, 6=Sunday)
        day_of_week = date.weekday()
        
        # Get doctor's schedule for this day
        schedules = Schedule.objects.filter(doctor=doctor, day_of_week=day_of_week)
        
        # Get existing appointments for this doctor on this date
        existing_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            status__in=['SCHEDULED', 'CONFIRMED']
        ).values_list('start_time', 'end_time')
        
        # Generate available slots (30-minute intervals)
        available_slots = []
        for schedule in schedules:
            current_time = datetime.combine(date, schedule.start_time)
            end_time = datetime.combine(date, schedule.end_time)
            
            while current_time < end_time:
                slot_end = current_time + timedelta(minutes=30)
                slot_end_time = slot_end.time()
                
                # Check if this slot overlaps with any existing appointment
                is_available = True
                for appt_start, appt_end in existing_appointments:
                    if (current_time.time() < appt_end and slot_end_time > appt_start):
                        is_available = False
                        break
                
                if is_available:
                    available_slots.append({
                        'start_time': current_time.time().strftime('%H:%M'),
                        'end_time': slot_end_time.strftime('%H:%M')
                    })
                
                current_time = slot_end
        
        return Response(available_slots)

# Template views
def appointment_list(request):
    # Mock data for demo
    upcoming_appointments = []
    past_appointments = []
    doctors = []
    
    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'doctors': doctors,
        'user': {'user_type': 'PATIENT'}  # Mock user
    }
    return render(request, 'appointments/appointment_list.html', context)

def appointment_detail(request, id):
    # Mock appointment detail
    appointment = {'id': id}
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})