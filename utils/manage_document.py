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
    try:
        url = "https://graph.facebook.com/v12.0/" + str(media_id) + "/messages?access_token=" + str(whatsapp_token)
        # payload = {
        #     "messaging_product": "whatsapp",
        #     "to": from_number,
        #     "text": { "body": msg_body }
        # }
        # headers = {"Content-Type": "application/json"}

        response = requests.get(url)
        if response.status_code == 200:
            print("URL retrieved successfully!")
            print('URL: ', response.url)
            out_url = response.url
            return out_url
        else:
            print("Error retrieved message:", response.text)
    except Exception as _e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERROR: ", exc_type, fname, exc_tb.tb_lineno)
        print("EXCEPTION: ", _e)


def download_media(url):
    try:
        url = "https://graph.facebook.com/v12.0/" + str(url) + "/messages?access_token=" + str(whatsapp_token)
        # payload = {
        #     "messaging_product": "whatsapp",
        #     "to": from_number,
        #     "text": { "body": msg_body }
        # }
        # headers = {"Content-Type": "application/json"}

        response = requests.get(url)
        if response.status_code == 200:
            print("URL download successfully!")
            print('RESPONSE: ', response)
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
    
    media_url = get_media_url(doc_id)
    download_media(media_url)
