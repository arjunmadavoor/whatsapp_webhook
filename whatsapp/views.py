from django.shortcuts import render

# Create your views here.

import json
import requests
from django.http import JsonResponse

from django.views import View
from django.http import HttpResponse

def sendMessageToWhatsApp(phone_number_id, token, from_number, msg_body):
    if msg_body == "Hi":
        msg_body = "Hi Welcome to DevOps!"
    elif msg_body == "Thanks":
        msg_body = "Welcome!"
    else:
        msg_body = "How can we help you?"
    
    url = "https://graph.facebook.com/v12.0/" + phone_number_id + "/messages?access_token=" + token
    payload = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "text": { "body": msg_body }
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Error sending message:", response.text)
class WhatsAppView(View):
    whatsapp_token = "EAAap7H54bbcBAGBKCDeAhzONIWARoFQk4XVjt2YwcA0BR1cqgV5LfT6nQgF6wnGmjrCySjRhjvUt3T2AiQdKJY2LMW1cJA3QiNnO7XEzp8lgv6n0ZCbUgxZANGU6loZBZCo0iOCZBUEd8KRZAYJbACy8CfPxieCDczsKEvGjqTfOuGaLNs4WHAKb5A1dk4Ns1SNJSZAUl01V6bMxX6ooj3W"
    verify_token = "mysampletoken24"
    def post(self, request):
        # Parse the request body from the POST
        body = request.body.decode('utf-8')

        # Check the Incoming webhook message
        print(body)

        # info on WhatsApp text message payload: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if 'object' in request.body:
            if 'entry' in request.body and request.body['entry'][0]['changes'] \
                and request.body['entry'][0]['changes'][0]['value']['messages'] \
                and request.body['entry'][0]['changes'][0]['value']['messages'][0]:

                phone_number_id = request.body['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
                from_number = request.body['entry'][0]['changes'][0]['value']['messages'][0]['from'] # extract the phone number from the webhook payload
                msg_body = request.body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'] # extract the message text from the webhook payload
                sendMessageToWhatsApp(phone_number_id, self.whatsapp_token, from_number, msg_body)

            return HttpResponse(status=200)
        else:
            # Return a '404 Not Found' if event is not from a WhatsApp API
            return HttpResponse(status=404)

    def get(self, request):
        """
        This will be the Verify Token value when you set up webhook
        """
        verify_token = request.GET.get('hub.verify_token')

        # Check if a token was sent
        if verify_token:
            # Check the token sent is correct
            if verify_token == self.verify_token:
                # Respond with 200 OK and challenge token from the request
                print('WEBHOOK_VERIFIED')
                return HttpResponse(request.GET.get('hub.challenge'))
            else:
                # Responds with '403 Forbidden' if verify tokens do not match
                return HttpResponse(status=403)
        else:
            # If there is no token in the request, return a '400 Bad Request' status code
            return HttpResponse(status=400)
        
    

