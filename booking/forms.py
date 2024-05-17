from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation

class BookClassForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['class_schedule', 'date']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.now().date():
            raise ValidationError("Cannot book a class for a past date.")
        return date