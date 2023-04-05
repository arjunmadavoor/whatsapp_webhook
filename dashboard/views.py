from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from whatsapp.models import UserData
from django.http import JsonResponse
from django.http import QueryDict

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

def registered_users(request):
    user_data = UserData.objects.filter(user_status="complete")
    return render(request, 'registered_users.html', {'user_data': user_data })

def verified_users(request):
    user_data = UserData.objects.filter(user_status="verified")
    return render(request, 'verified_users.html', {'user_data': user_data })

def pending_users(request):
    user_data = UserData.objects.filter(user_status__in=['notstarted', 'started'],)
    return render(request, 'pending_users.html', {'user_data': user_data })

def handler404(request, exception):
    return render(request, '404.html', status=404)

def verify_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            # user_id = user_id
            user = UserData.objects.get(pk=user_id)
            user.user_status = "verified"
            user.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    except:
        return JsonResponse({'success': False})

def delete_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            # user_id = user_id
            user = UserData.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    except:
        return JsonResponse({'success': False})
    
def edit_user(request):
    try:
        if request.method == 'POST':
            serialized_data = request.POST.urlencode()
            # convert data to Dict 
            data_dict = QueryDict(serialized_data)
            user_id = data_dict.get('id')
            user_data = UserData.objects.get(pk=user_id)
            user_data.user_status = data_dict.get('status')
            question_data = user_data.question_data
            question_data[0]['answer'] = data_dict.get('name')
            question_data[1]['answer'] = data_dict.get('email')
            question_data[2]['answer'] = data_dict.get('mobile')
            question_data[3]['answer'] = data_dict.get('aadhar')
            question_data[4]['answer'] = data_dict.get('pan')
            user_data.question_data = question_data
            user_data.save()

            return JsonResponse({'success': True, 'data': data_dict})
        return JsonResponse({'success': False})
    except:
        return JsonResponse({'success': False})

