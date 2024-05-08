from django.shortcuts import render
from django.views.generic import TemplateView

class BookingView(TemplateView):
    template_name = 'booking.html' 


