from django.urls import path
from .views import BookingView, FetchClassSchedules, BookClass

urlpatterns = [
    path('booking/', BookingView.as_view(), name='booking'),
    path('fetch-schedules/', FetchClassSchedules.as_view(), name='fetch_schedules'),
    path('book-class/', BookClass.as_view(), name='book_class')
]