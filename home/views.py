from django.shortcuts import render

# Create your views here.
from whatsapp.models import ChatbotData

def home_view(request):
    chat_data = ChatbotData.objects.all()
    return render(request, 'home.html', {'chat_data': chat_data})
