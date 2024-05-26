from django.urls import path
from .views import BookingPageView, FetchClassSchedules, BookClass, DeleteReservation, UserReservationsView, MyBookingPageView

urlpatterns = [
    path('booking/', BookingPageView.as_view(), name='booking'),
    path('fetch-schedules/', FetchClassSchedules.as_view(), name='fetch_schedules'),
    path('book-class/', BookClass.as_view(), name='book_class'),
    path('delete-reservation/', DeleteReservation.as_view(), name='delete_reservation'),
    path('mybookings/', MyBookingPageView.as_view(), name='mybookings'),
    path('reservations/', UserReservationsView.as_view(), name='user_reservations'),
]