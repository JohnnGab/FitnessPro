from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, F, Q
from .models import ClassSchedule, Reservation
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

class BookingView(TemplateView):
    template_name = 'booking.html'

class FetchClassSchedules(View):
    def get(self, request, *args, **kwargs):
        selected_date_str = request.GET.get('date')
        if selected_date_str:
            try:
                selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')
                day_name = selected_date.strftime("%A")
                schedules = ClassSchedule.objects.filter(weekday__day_name=day_name).annotate(
                    booked=Count('reservation_set__id', filter=Q(reservation_set__date=selected_date)),
                    available=F('capacity') - F('booked')
                ).values('id', 'classes__class_name', 'time', 'available', 'capacity')
                return JsonResponse(list(schedules), safe=False)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
        return JsonResponse({'error': 'Date parameter is required'}, status=400)

class BookClass(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect to login page if not authenticated

    def post(self, request, *args, **kwargs):
        user = request.user
        schedule_id = request.POST.get('schedule_id')
        date = request.POST.get('date')

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
            return JsonResponse({'status': 'error', 'message': 'Schedule not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
