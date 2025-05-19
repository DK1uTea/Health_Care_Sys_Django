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
    
    # Add mock doctors for demonstration
    doctors = [
        {'id': 1, 'name': 'John Smith', 'specialization': 'Cardiology'},
        {'id': 2, 'name': 'Sara Johnson', 'specialization': 'Neurology'},
        {'id': 3, 'name': 'David Chen', 'specialization': 'Pediatrics'},
        {'id': 4, 'name': 'Maria Rodriguez', 'specialization': 'Orthopedics'},
        {'id': 5, 'name': 'Robert Wilson', 'specialization': 'Dermatology'}
    ]
    
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

def book_appointment(request):
    """Handle appointment booking form submission"""
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        reason = request.POST.get('reason')
        
        # In a real app, validate the data and create a real Appointment object
        # For demo, just show success and redirect
        
        # Example of creating a real appointment (commented out for mock version)
        # try:
        #     doctor = Doctor.objects.get(id=doctor_id)
        #     appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        #     start_time, end_time = time_slot.split('-')
        #     
        #     appointment = Appointment.objects.create(
        #         patient_id=request.user.id,  # In a real app
        #         doctor=doctor,
        #         appointment_date=appointment_date,
        #         start_time=start_time,
        #         end_time=end_time,
        #         reason=reason,
        #         status='SCHEDULED'
        #     )
        # except Exception as e:
        #     # Handle errors
        #     return render(request, 'appointments/error.html', {'error': str(e)})
        
        # For now, just return a success page
        return render(request, 'appointments/booking_success.html', {
            'appointment': {
                'doctor_name': next((d['name'] for d in [
                    {'id': 1, 'name': 'John Smith'},
                    {'id': 2, 'name': 'Sara Johnson'},
                    {'id': 3, 'name': 'David Chen'},
                    {'id': 4, 'name': 'Maria Rodriguez'},
                    {'id': 5, 'name': 'Robert Wilson'}
                ] if str(d['id']) == doctor_id), 'Unknown Doctor'),
                'date': date_str,
                'time': time_slot,
                'reason': reason
            }
        })
    
    # If not a POST request, redirect to appointment list
    return redirect('appointment_list')