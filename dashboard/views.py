from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from whatsapp.models import UserData

# Create your views here.
@login_required
def dashboard_view(request):
    user_data = UserData.objects.all()
    total_user = user_data.count()
    total_complete = UserData.objects.filter(user_status='complete').count()
    total_started = UserData.objects.filter(user_status='started').count()
    total_notstarted = UserData.objects.filter(user_status='notstarted').count()
    total_verified = UserData.objects.filter(user_status='verified').count()

    
    context = {
        'user_data': user_data,
        'total_user': total_user,
        'total_complete': total_complete,
        'total_notstarted': total_notstarted,
        'total_verified': total_verified,
        'total_started': total_started,
        # add other key-value pairs as needed
    }
    return render(request, 'index.html', context)
  
def all_users(request):
    user_data = UserData.objects.all()
    return render(request, 'all_users.html', {'user_data': user_data })

def handler404(request, exception):
    return render(request, '404.html', status=404)