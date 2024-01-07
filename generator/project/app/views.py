from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import generate_data  # Assuming the code is in models.py

def index(request):
    if request.method == 'GET':
        generated_data = generate_data()
        return JsonResponse(generated_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
