from django.shortcuts import render

# Create your views here.
import os
import json
import requests
from django.http import JsonResponse

from django.views import View
from django.http import HttpResponse
from dotenv import load_dotenv
load_dotenv()
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
    whatsapp_token = os.getenv('whatsapp_token')
    verify_token = os.getenv('verify_token')
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
        Handles GET requests to verify the webhook
        """
        # Update your verify token
        verify_token = "mysampletoken24"
        # Parse params from the webhook verification request
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        
        # Check if a token and mode were sent
        try:
            if mode and token:
                # Check the mode and token sent are correct
                if mode == "subscribe" and token == verify_token:
                    # Respond with 200 OK and challenge token from the request
                    print("WEBHOOK_VERIFIED")
                    return HttpResponse(challenge, status=200)
                else:
                    # Responds with '403 Forbidden' if verify tokens do not match
                    return HttpResponse(status=403)
            else:
                return HttpResponse(status=404)
        except Exception as _e:
            print(_e)
        
    

