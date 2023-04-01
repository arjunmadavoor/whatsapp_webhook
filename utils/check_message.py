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

def open_ai(prompt):
    """
    Generate text using the OpenAI API.

    Args:
        prompt (str): The prompt for generating text.

    Returns:
        str: The generated text.

    Raises:
        Exception: If an error occurs while generating text.
    """
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
    """
    Send a message via WhatsApp using the Facebook Graph API.

    Args:
        phone_number_id (int): The Facebook ID of the phone number to send the message to.
        from_number (str): The phone number to send the message.
        msg_body (str): The body of the message to send.
        whatsapp_token (str): The access token for the WhatsApp Business API.

    Returns:
        None.

    Raises:
        Exception: If an error occurs while sending the message.
    """
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
    """
    Checks if a message exists for a given mobile number in the database,
    updates it if it exists, creates a new one if it does not.
    Also sends a message back to the user.
    """
    whatsapp_token = env('whatsapp_token')
    print("phone_number_id: ", phone_number_id)
    print("from_number: ", from_number)
    print("msg_body: ", msg_body)
    
    manage_user(phone_number_id, from_number, whatsapp_token, msg_body)    

        
        
        
# CheckUserData:

# IF not user:
    # Send Welcome Message:
    
# IF user:
    # if message == "START":
        # Ask first question and save to db
    # elif db contains question array aray and check q is fill and a in empty then consider as answer and ask next question
    
    # elif message == "STOP":
        # drop the user from table
    # else:
        # something went wrong!
def manage_user(phone_number_id, from_number, whatsapp_token, msg_body):
    questions = [
        'Please type your name: ',
        'Type your email id: ',
        'Type your mobile number: ',
    ]
    try:
        user_data = UserData.objects.get(mobile_number=from_number)
    except UserData.DoesNotExist:
        msg_body = "Hello, Welcome to Demat account creation chatbot. PLease type START to create account. Type STOP to end the process."
        sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
        question_data = []
        data = UserData(mobile_number=from_number, question_data=question_data, created_date=datetime.now(), user_status="notstarted")
        data.save()
    else:
        user_question = user_data.question_data
        print("USER QUESTION: ", user_question)
        print(type(user_question))
        
        if str(msg_body) == "START" and len(user_question) == 0:
            msg_body = questions[0]
            question_data = [{
                "question": msg_body,
                "answer": "",
                "timestamp": str(datetime.now())
            }]
            user_status="started"
            user_data.question_data = question_data
            user_data.user_status = user_status
            user_data.save()
            sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
        elif str(msg_body) == "START" and len(user_question) != 0:
            msg_body = "You have entered a invalid output. Please check!"
            sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
        elif str(msg_body) == "STOP":
            if user_data.user_status != "complete":
                question_data = []
                msg_body = "Okay. We are deleting all your progress...Type START again if you want to register again!"
                user_status="notstarted"
                user_data.question_data = question_data
                user_data.user_status = user_status
                user_data.save()
                sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
        else:
            question_number = len(user_data.question_data)
            print('question_number ', question_number)
            if question_number < 3:
                isAnswered = user_data.question_data[question_number - 1]['answer']
                if isAnswered != "":
                    msg_body = questions[question_number]
                    question_data = user_data.question_data
                    question_data.append({
                        "question": msg_body,
                        "answer": "",
                        "timestamp": str(datetime.now())
                    })
                    user_data.save()
                    sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
                else:
                    question_data = user_data.question_data[question_number - 1]
                    question_data['answer'] = str(msg_body)
                    user_data.save()
                    msg_body = questions[question_number + 1]
                    question_data = user_data.question_data
                    question_data.append({
                        "question": msg_body,
                        "answer": "",
                        "timestamp": str(datetime.now())
                    })
                    user_data.save()
                    sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
                    # if question_number == 3:
                    #     user_status = user_data.user_status
                    #     user_status = "complete"
                    #     user_data.save()
                    #     msg_body = "Thank you for registering with us. Your application is submited. We will send you a confirmation message once completed."
                    #     sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)
            
            else:
                msg_body = "You have succesfuly registered. Please conatct the nearest branch if any query. Thankyou!"
                sendMessage(phone_number_id, from_number, msg_body, whatsapp_token)

