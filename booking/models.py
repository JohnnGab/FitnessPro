from django.db import models
from django.conf import settings

class Classes(models.Model):
    class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.class_name

class Weekday(models.Model):
    day_name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.day_name

class ClassSchedule(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    time = models.TimeField()
    duration = models.IntegerField()
    capacity = models.IntegerField()

    class Meta:
        unique_together = ('classes', 'weekday', 'time')

    def get_duration_display(self):
        """Converts duration from minutes to a formatted string."""
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours > 0:
            return f"{hours}hr {minutes}min" if minutes else f"{hours}hr"
        return f"{minutes}min"

    def __str__(self):
        return f"{self.classes} on {self.weekday} at {self.time.strftime('%H:%M')}"
    
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'class_schedule', 'date')

    def __str__(self):
        return f"{self.user.username} reserved {self.class_schedule} on {self.date}"