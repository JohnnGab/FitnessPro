from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import json

def home(request):
    return render(request, 'index.html')