

import os, sys
import json
import requests
from django.http import JsonResponse
from datetime import datetime
import openai
from django.conf import settings
from whatsapp.models import ChatbotData
import environ
env = environ.Env()
env_path = os.path.join(settings.BASE_DIR, '.env')
environ.Env.read_env(env_file=env_path)

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
        return text
      
    except Exception as _e:
        print(_e)
  

def sendMessage(phone_number_id, from_number, msg_body, whatsapp_token):
    try:
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
    except Exception as _e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERROR: ", exc_type, fname, exc_tb.tb_lineno)
        print("EXCEPTION: ", _e)
        
        
def checkMessage(phone_number_id, from_number, msg_body):
    whatsapp_token = env('whatsapp_token')
    questions = [
        'Please type your name: ',
        'Type your email id: ',
        'Type your mobile number: ',
        'Type your Aadhar number: ',
        'Type your Date of birth: '
    ]
    print("phone_number_id: ", phone_number_id)
    print("from_number: ", from_number)
    print("msg_body: ", msg_body)
    
    try:
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
                    # question_data = json.loads(data.question_data)
                    
                    question_data = data.question_data
                    question_data.append({
                        "question": str(in_msg),
                        "answer": str(out_msg),
                        "timestamp": str(datetime.now())
                    })
                    # Update the question_data field with the updated JSON object
                    data.question_data = question_data
                    data.save()
                else:
                    # If the question_data field is empty, create a new JSON object with the given question and answer
                    question_data = [{
                        "question": str(in_msg),
                        "answer": str(out_msg),
                        "timestamp": str(datetime.now())
                    }]
                    data.question_data = question_data
                    data.save()
        else:
            # If no instances are found with the given mobile number, create a new instance with the given mobile number and question data
            question_data = [{
                "question": str(in_msg),
                "answer": str(out_msg),
                "timestamp": str(datetime.now())
            }]
            data = ChatbotData(mobile_number=from_number, question_data=question_data)
            data.save()
        # chatbot_data = ChatbotData(mobile_number=from_number, question_data=question_data)
        # chatbot_data.save()
        sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
            
    except Exception as _e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERROR: ", exc_type, fname, exc_tb.tb_lineno)