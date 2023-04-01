from django.contrib import admin

# Register your models here.
from .models import UserData

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'user_status', 'created_date')
    search_fields = ('mobile_number',)
    list_filter = ('user_status',)

admin.site.register(UserData, UserDataAdmin)
