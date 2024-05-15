from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, F, Q
from .models import ClassSchedule, Reservation
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.generic import TemplateView
from .forms import BookClassForm

class BookingView(TemplateView):
    template_name = 'booking.html'

class FetchClassSchedules(View):
    
    def get(self, request, *args, **kwargs):
        selected_date_str = request.GET.get('date')
        if not selected_date_str:
            return self.error_response('Date parameter is required', status=400)

        try:
            selected_date = self.parse_date(selected_date_str)
            schedules = self.get_schedules(selected_date)
            return JsonResponse(list(schedules), safe=False)
        except ValidationError as e:
            return self.error_response(str(e), status=400)

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Invalid date format. Please use YYYY-MM-DD.')

    def get_schedules(self, selected_date):
        day_name = selected_date.strftime("%a")
        schedules = ClassSchedule.objects.filter(weekday__day_name=day_name).annotate(
            booked=Count('reservation__id', filter=Q(reservation__date=selected_date)),
            available=F('capacity') - F('booked'))
        
        schedule_list = []
        for schedule in schedules:
            schedule_dict = {
            'id': schedule.id,
            'classes__class_name': schedule.classes.class_name,
            'time': schedule.time.strftime('%H:%M:%S'),
            'duration': schedule.get_duration_display(),
            'available': schedule.available,
            'capacity': schedule.capacity
        }
            schedule_list.append(schedule_dict)
    
        return schedule_list

    def error_response(self, message, status=400):
        return JsonResponse({'error': message}, status=status)

class BookClass(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = BookClassForm(request.POST)
        if form.is_valid():
            try:
                user = request.user
                schedule_id = form.cleaned_data['schedule_id']
                date = form.cleaned_data['date']
                return self.book_class(user, schedule_id, date)
            except ValidationError as e:
                return self.error_response(str(e), status=400)
            except Exception as e:
                return self.error_response(str(e), status=500)
        else:
            return self.error_response(form.errors.as_json(), status=400)

    def book_class(self, user, schedule_id, date):
        try:
            with transaction.atomic():
                schedule = ClassSchedule.objects.select_for_update().get(id=schedule_id)
                reservation_count = Reservation.objects.filter(class_schedule=schedule, date=date).count()
                if reservation_count < schedule.capacity:
                    Reservation.objects.create(user=user, class_schedule=schedule, date=date)
                    available_spots = schedule.capacity - reservation_count - 1
                    return JsonResponse({'status': 'success', 'available_spots': available_spots})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Class is fully booked'})
        except ObjectDoesNotExist:
            raise ValidationError('Schedule not found')

    def error_response(self, message, status=400):
        return JsonResponse({'error': message}, status=status)