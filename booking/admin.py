from django.contrib import admin
from .models import Classes, Weekday, ClassSchedule, Reservation

admin.site.register(Classes)
admin.site.register(Weekday)
admin.site.register(ClassSchedule)
admin.site.register(Reservation)