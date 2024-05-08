from django.urls import path
from .views import BookingView

urlpatterns = [
    path('booking/', BookingView.as_view(), name='booking'),
]