from django.shortcuts import render

# Create your views here.

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook(request):
    # Get the JSON payload from the request
    
    json_data = json.loads(request.body.decode('utf-8'))

    # Handle the incoming request
    # TODO: Implement your own webhook logic here

    # Send a response back to WhatsApp
    response = {'status': 'success'}
    return JsonResponse(response)
