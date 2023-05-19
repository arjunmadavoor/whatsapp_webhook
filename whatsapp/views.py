from django.shortcuts import render
# Create your views here.
import os
import json
from django.http import JsonResponse

from django.views import View
from django.http import HttpResponse
from django.conf import settings
import environ
env = environ.Env()
env_path = os.path.join(settings.BASE_DIR, '.env')
environ.Env.read_env(env_file=env_path)

from utils.check_message import checkMessage



import os
import openai


class WhatsAppView(View):
    verify_token = env('verify_token')
    def post(self, request):
        whatsapp_token = env('whatsapp_token')
        
        # Parse the request body from the POST
        body_str = request.body.decode('utf-8')
        body_obj = json.loads(body_str)
        
        print('######BOdyyy######')
        # Check the Incoming webhook message
        print("Body Object: ", body_obj)

        # info on WhatsApp text message payload: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if 'object' in body_obj:
            if 'entry' in body_obj and body_obj['entry'][0]['changes'] \
                and body_obj['entry'][0]['changes'][0]['value']['messages'] \
                and body_obj['entry'][0]['changes'][0]['value']['messages'][0]:
                if body_obj['entry'][0]['changes'][0]['value']['messages'][0]['type'] == 'text':
                    phone_number_id = body_obj['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
                    from_number = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['from'] # extract the phone number from the webhook payload
                    msg_body = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'] # extract the message text from the webhook payload
                    checkMessage(str(phone_number_id), str(from_number), str(msg_body))
                else:
                    print('######Attachment######')

            return HttpResponse(status=200)
        else:
            # Return a '404 Not Found' if event is not from a WhatsApp API
            return HttpResponse(status=404)

    def get(self, request):
        """
        Handles GET requests to verify the webhook
        """
        # Update your verify token
        verify_token = env('verify_token')
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
        