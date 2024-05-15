from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError

class BookClassForm(forms.Form):
    schedule_id = forms.IntegerField()
    date = forms.DateField(input_formats=['%Y-%m-%d'])

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.now().date():
            raise ValidationError("Cannot book a class for a past date.")
        return date