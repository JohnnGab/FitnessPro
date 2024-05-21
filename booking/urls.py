from django.urls import path
from .views import BookingView, FetchClassSchedules, BookClass, DeleteReservation

urlpatterns = [
    path('booking/', BookingView.as_view(), name='booking'),
    path('fetch-schedules/', FetchClassSchedules.as_view(), name='fetch_schedules'),
    path('book-class/', BookClass.as_view(), name='book_class'),
    path('delete-reservation/', DeleteReservation.as_view(), name='delete_reservation'),
]