from django.db import models

# Create your models here.

class ChatbotData(models.Model):
    mobile_number = models.CharField(max_length=20)
    question_data = models.JSONField(default=dict)
