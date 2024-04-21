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
from .forms import CustomUserCreationForm, CustomAuthForm
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_GET

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
        
        return redirect('home')

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
    
class CustomLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = 'signin.html'

    def form_valid(self, form):
        # Perform the login operation
        super().form_valid(form)
        # Return a JSON response indicating success
        return JsonResponse({"success": True, "message": "Login successful"})

    def form_invalid(self, form):
        # Get all form errors
        errors = form.errors.as_json()
        # Return a JSON response indicating an error with the form data
        return JsonResponse({"success": False, "errors": errors}, status=400)
    
@require_GET
def check_authentication_status(request):
    return JsonResponse({'isAuthenticated': request.user.is_authenticated})