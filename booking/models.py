from django.db import models

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
