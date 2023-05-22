import os, sys
import json
import requests
from django.http import JsonResponse
from datetime import datetime
import openai
from django.conf import settings
from whatsapp.models import ChatbotData
from whatsapp.models import UserData
import environ
env = environ.Env()
env_path = os.path.join(settings.BASE_DIR, '.env')
environ.Env.read_env(env_file=env_path)


def get_media_url(media_id):
    print("Inside get_media_url function: ", media_id)
    whatsapp_token = env('whatsapp_token')
    try:
        url = "https://graph.facebook.com/v12.0/" + str(media_id)
        # payload = {
        #     "messaging_product": "whatsapp",
        #     "to": from_number,
        #     "text": { "body": msg_body }
        # }
        headers = {
            "Authorization": f"Bearer {str(whatsapp_token)}"
        }


        response = requests.get(url, headers=headers)
        print(response.json())
        if response.status_code == 200:
            print("URL retrieved successfully!")
            response_out = response.json()
            print('URL: ', response_out['url'])
            return response_out['url']
        else:
            print("Error retrieved message:", response.text)
    except Exception as _e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERROR: ", exc_type, fname, exc_tb.tb_lineno)
        print("EXCEPTION: ", _e)


def download_media(url):
    whatsapp_token = env('whatsapp_token')
    try:
        url = "https://graph.facebook.com/v12.0/" + str(url)
        # payload = {
        #     "messaging_product": "whatsapp",
        #     "to": from_number,
        #     "text": { "body": msg_body }
        # }
        # headers = {"Content-Type": "application/json"}
        headers = {
            "Authorization": f"Bearer {str(whatsapp_token)}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("URL download successfully!")
            print('RESPONSE: ', response.json())
        else:
            print("Error download message:", response.text)
    except Exception as _e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERROR: ", exc_type, fname, exc_tb.tb_lineno)
        print("EXCEPTION: ", _e)

def manageDocument(body_obj):
    """
    check document messages
    """
    whatsapp_token = env('whatsapp_token')
    phone_number_id = body_obj['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
    from_number = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['from']
    doc_name = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['document']['filename']
    doc_id = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['document']['id']
    mime_type = body_obj['entry'][0]['changes'][0]['value']['messages'][0]['document']['mime_type']
    print("phone_number_id: ", phone_number_id)
    print("from_number: ", from_number)
    print("doc_name: ", doc_name)
    print("doc_id: ", doc_id)
    print("mime_type: ", mime_type)
    
    media_url = get_media_url(str(doc_id))
    download_media(str(media_url))
