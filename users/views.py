from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse

class CreateAccountView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'createaccount.html'
    
    def form_valid(self, form):
        # Save the form data and get the user instance
        new_user = form.save()

        # Authenticate the user programmatically
        authenticated_user = authenticate(
            self.request,
            email=new_user.email, 
            password=form.cleaned_data.get('password1')
        )

         # Log in the authenticated user
        if authenticated_user:
            login(self.request, authenticated_user)
        
        # Define the redirect URL after successful registration
        redirect_url = reverse('home')

        # Return success response as JSON with redirect URL
        return JsonResponse({'success': True, 'message': 'Registration successful', 'redirect_url': redirect_url}, status=201)

    def form_invalid(self, form):
        # Collect form errors
        errors = form.errors.as_data()

        # Prepare a dictionary to hold field-specific error messages
        error_messages = {}
        for field, field_errors in errors.items():
            # Convert each Django ValidationError to a readable message
            error_messages[field] = [error.message for error in field_errors]

        # Return error response as JSON
        return JsonResponse({'success': False, 'errors': error_messages}, status=400)
    

def SigninView(request):
    # This view just renders the signin.html template.
    return render(request, 'signin.html')