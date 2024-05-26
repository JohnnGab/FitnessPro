import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, F, Q
from .models import ClassSchedule, Reservation
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from django.views.generic import TemplateView, ListView 
from .forms import BookClassForm
from django.urls import reverse_lazy, reverse

class BookingView(TemplateView):
    template_name = 'booking.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/users/signin/')
        return super().dispatch(request, *args, **kwargs)

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
            reservation = Reservation.objects.filter(class_schedule=schedule, date=selected_date, user=self.request.user).first()
            schedule_dict = {
            'id': schedule.id,
            'classes__class_name': schedule.classes.class_name,
            'time': schedule.time.strftime('%H:%M:%S'),
            'duration': schedule.get_duration_display(),
            'available': schedule.available,
            'capacity': schedule.capacity,
            'reservation_id': reservation.id if reservation else None
        }
            schedule_list.append(schedule_dict)
        return schedule_list

    def error_response(self, message, status=400):
        return JsonResponse({'error': message}, status=status)

class BookClass(LoginRequiredMixin, View):
    login_url = reverse_lazy('signin')
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            form = BookClassForm(data)
            if form.is_valid():
                try:
                    return self.book_class(request.user, form)
                except ValidationError as e:
                    return self.error_response(str(e), status=400)
                except Exception as e:
                    return self.error_response(str(e), status=500)
            else:
                return self.error_response(form.errors.as_json(), status=400)
        except json.JSONDecodeError:
            return self.error_response("Invalid JSON data", status=400)

    def book_class(self, user, form):
        try:
            with transaction.atomic():
                schedule = ClassSchedule.objects.select_for_update().get(id=form.cleaned_data['class_schedule'].id)
                date = form.cleaned_data['date']
                reservation_count = Reservation.objects.filter(class_schedule=schedule, date=date).count()
                if reservation_count < schedule.capacity:
                    reservation = form.save(commit=False)
                    reservation.user = user
                    reservation.save()
                    available_spots = schedule.capacity - reservation_count - 1
                    return JsonResponse({'status': 'success', 'reservation_id': reservation.id, 'available_spots': available_spots})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Class is fully booked'})
        except ObjectDoesNotExist:
            raise ValidationError('Schedule not found')

    def error_response(self, message, status=400):
        return JsonResponse({'error': message}, status=status)

class DeleteReservation(LoginRequiredMixin, View):
    login_url = reverse_lazy('signin')

    def delete(self, request, *args, **kwargs):
        try:
            reservation_id = request.GET.get('id')
            if not reservation_id:
                return self.error_response('Reservation ID is required', status=400)

            reservation = Reservation.objects.get(id=reservation_id, user=request.user)
            reservation.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except ObjectDoesNotExist:
            return self.error_response('Reservation not found', status=404)
        except PermissionDenied:
            return self.error_response('Permission denied', status=403)
        except Exception as e:
            return self.error_response(str(e), status=500)

    def error_response(self, message, status=400):
        return JsonResponse({'error': message}, status=status)

class BookingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mybookings.html'
    login_url = reverse_lazy('signin')


class UserReservationsView(ListView):
    model = Reservation

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related('class_schedule', 'class_schedule__classes')

    def render_to_response(self, context, **response_kwargs):
        reservations = context['object_list']
        data = []
        for reservation in reservations:
            data.append({
                'reservation_id': reservation.id,
                'date': reservation.date,
                'class_name': reservation.class_schedule.classes.name,
                'time': reservation.class_schedule.time.strftime('%H:%M'),
                'duration': reservation.class_schedule.get_duration_display(),
            })
        return JsonResponse(data, safe=False, **response_kwargs)