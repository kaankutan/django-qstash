from django.shortcuts import render
from django.http import HttpResponse
from django_qstash.results.models import TaskResult
from django.utils import timezone
from .tasks import send_welcome_notification, send_reminder_notification
import json

# Create your views here.

def register_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        # Send immediate welcome
        welcome_task = send_welcome_notification.delay(email)
        
        # Schedule reminder for 24 hours later
        reminder_task = send_reminder_notification.apply_async(
            args=[email],
            countdown=86400  # 24 hours
        )
        
        return render(request, 'notifications/registration_success.html', {
            'email': email,
            'welcome_task_id': welcome_task.task_id,
            'reminder_task_id': reminder_task.task_id
        })
    
    return render(request, 'notifications/register.html')

def task_dashboard(request):
    # Get all tasks from the last 24 hours
    recent_tasks = TaskResult.objects.filter(
        date_done__gte=timezone.now() - timezone.timedelta(days=1)
    ).order_by('-date_done')
    
    # Format the JSON results
    formatted_tasks = []
    for task in recent_tasks:
        try:
            # First parse the outer JSON string
            result_dict = json.loads(task.result)
            # Then parse the inner 'result' field which is also a JSON string
            inner_result = json.loads(result_dict['result'])
            
            formatted_tasks.append({
                'task_id': task.task_id,
                'status': task.status,
                'result': inner_result,
                'date_done': task.date_done
            })
        except:
            formatted_tasks.append({
                'task_id': task.task_id,
                'status': task.status,
                'result': task.result,
                'date_done': task.date_done
            })
    
    return render(request, 'notifications/task_dashboard.html', {
        'tasks': formatted_tasks
    })
