from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
    
    def clean_email(self):
        User = get_user_model()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already registered.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        has_digit = any(char.isdigit() for char in password)
        has_uppercase = any(char.isupper() for char in password)
        allowed_symbols = set("!@#$%^&*()-_+=~`|\\[{]};:'\",<.>/?")
        has_symbol = any(char in allowed_symbols for char in password)

    # If any condition fails, raise a validation error with a comprehensive message
        if not (has_digit and has_uppercase and has_symbol):
            raise forms.ValidationError(
            "Password must contain at least 1 uppercase letter, a number, a symbol and must be at least 8 charachters."
        )

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")