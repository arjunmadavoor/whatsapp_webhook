from django.shortcuts import render
from .models import ChatbotData
# Create your views here.
import os
import json
import requests
from django.http import JsonResponse
from datetime import datetime

from django.views import View
from django.http import HttpResponse
import environ
env = environ.Env()
environ.Env.read_env(env_file='/home/arjunmdr/whatsapp_webhook/.env')
#environ.Env.read_env(env_file='/Users/user/Documents/Projects/whatsapp_env/whatsapp_webhook/.env')


import os
import openai

def open_ai(prompt):
    try:
        openai.api_key = env("OPENAI_API_KEY")
        response: dict = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=1075,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )
        choices: dict = response.get('choices')[0]
        text = choices.get('text')
    except Exception as _e:
        print(_e)
        
    return text
        
def sendMessage(phone_number_id, from_number, msg_body, whatsapp_token):
    in_msg = msg_body
    msg_body = open_ai(msg_body)
    out_msg = str(msg_body)
    data_with_mobile_number = ChatbotData.objects.filter(mobile_number=from_number)
    if data_with_mobile_number.exists():
        # Iterate over the instances with the given mobile number and update the question_data field
        for data in data_with_mobile_number:
            # Check if the question_data field is already a JSON object
            if data.question_data:
                # Parse the existing JSON data and append the new question and answer
                question_data = json.loads(data.question_data)
                question_data.append({
                    "question": in_msg,
                    "answer": out_msg,
                    "timestamp": str(datetime.now())
                })
                # Update the question_data field with the updated JSON object
                data.question_data = json.dumps(question_data)
                data.save()
            else:
                # If the question_data field is empty, create a new JSON object with the given question and answer
                question_data = [{
                    "question": in_msg,
                    "answer": out_msg,
                    "timestamp": str(datetime.now())
                }]
                data.question_data = json.dumps(question_data)
                data.save()
    else:
        # If no instances are found with the given mobile number, create a new instance with the given mobile number and question data
        question_data = [{
            "question": in_msg,
            "answer": out_msg,
            "timestamp": str(datetime.now())
        }]
        data = ChatbotData(mobile_number=from_number, question_data=json.dumps(question_data))
        data.save()
    chatbot_data = ChatbotData(mobile_number=from_number, question_data=question_data)
    chatbot_data.save()
    url = "https://graph.facebook.com/v12.0/" + str(phone_number_id) + "/messages?access_token=" + str(whatsapp_token)
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

def checkMessage(phone_number_id, from_number, msg_body):
    whatsapp_token = env('whatsapp_token')
    questions = [
        'Please type your name: ',
        'Type your email id: ',
        'Type your mobile number: ',
        'Type your Aadhar number: ',
        'Type your Date of birth: '
    ]
    try:
        print("phone_number_id: ", phone_number_id)
        print("from_number: ", from_number)
        print("msg_body: ", msg_body)
    
        sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)

    except Exception as _e:
        print("ERROR: ", _e)
        
class WhatsAppView(View):
    verify_token = env('verify_token')
    def post(self, request):
        whatsapp_token = env('whatsapp_token')
        
        # Parse the request body from the POST
        body_str = request.body.decode('utf-8')
        body_obj = json.loads(body_str)

        # Check the Incoming webhook message
        print("Body Object: ", body_obj)

        # info on WhatsApp text message payload: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if 'object' in body_obj:
            if 'entry' in body_obj and body_obj['entry'][0]['changes'] \
                and body_obj['entry'][0]['changes'][0]['value']['messages'] \
                and body_obj['entry'][0]['changes'][0]['value']['messages'][0]:

                phone_number_id = body_obj['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
                from_number = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['from'] # extract the phone number from the webhook payload
                msg_body = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'] # extract the message text from the webhook payload
                checkMessage(str(phone_number_id), str(from_number), str(msg_body))

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
        
    

