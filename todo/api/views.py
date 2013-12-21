from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from todo.api.urls import urlpatterns
from todo.task.models import *
from datetime import datetime

# Create your views here.
@api_view(['GET'])
@permission_classes((AllowAny,))
def hello_world(request):
    """<h2>Welcome to Bluebear!</h2>"""

    name = ""

    if request.user:
        name = request.user.username

    link = "http://%s%s" % (request.META['HTTP_HOST'], reverse('todo.api.views.api_list'))

    return Response(
        {"message": "GRRR! %s" % name, "api_list": link})


@api_view(['GET'])
def api_list(request):
    """<h3>Log in is required to view this page.</h3>
    """
    apis = []
    for url in urlpatterns:
        apis.append("http://%s%s" % (request.META['HTTP_HOST'], reverse(url._callback_str)))

    return Response({"apis": apis})

@api_view(['GET'])
def tasks(request):
    """<h3>Get task list</h3>
    <h4>Headers</h4>
    <ul>
    <li>Authorization (Required, Basic Auth see http://tools.ietf.org/html/rfc2617)</li>
    </ul>
    <h4>Parameters</h4>
    <ul>
    <li>sorted_by (Optional default=due_date; available values: due_date, priority)</li>
    </ul>
    """
    try:
        tasks = Task.objects.filter(created_by=request.user).extra(select={
                                                                           'due_date_is_null': 'due_date IS NULL',
                                                                           })
        
        try:
            sorted_by = request.QUERY_PARAMS['sorted_by']
            
            if sorted_by == 'priority':
                tasks = tasks.order_by('-priority', 'due_date_is_null', 'due_date', 'id')
            else:
                tasks = tasks.order_by('due_date_is_null', 'due_date', '-priority', 'id')
        except:
            tasks = tasks.order_by('due_date_is_null', 'due_date', '-priority', 'id')
        
        task_dict = []
        
        for task in tasks:
            context = task.to_dict()
            task_dict.append(context)
        
        return Response({"tasks": task_dict})
    except MultiValueDictKeyError:
        return Response({"message": "Missing parameter"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_task(request):
    """<h3>Add task.</h3>
    <h4>Headers</h4>
    <ul>
    <li>Authorization (Required, Basic Auth see http://tools.ietf.org/html/rfc2617)</li>
    </ul>
    <h4>Parameters</h4>
    <ul>
    <li>name (Required)</li>
    </ul>
    """
    try:
        task = Task()
        task.name = request.DATA['name']
        
        if len(task.name) > 2000:
            return Response({"message": "Invalid task's name. Name must not longer than 2000 characters.", "error_field": "name"}, status=status.HTTP_400_BAD_REQUEST)
        elif len(task.name) == 0:
            raise MultiValueDictKeyError
            
        task.created_by = request.user
        
        task.save()
        
        return Response({"message": "New task successfully added.", "task": task.to_dict()})
    except MultiValueDictKeyError:
        return Response({"message": "Missing parameter"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_task(request):
    """<h3>Delete task.</h3>
    <h4>Headers</h4>
    <ul>
    <li>Authorization (Required, Basic Auth see http://tools.ietf.org/html/rfc2617)</li>
    </ul>
    <h4>Parameters</h4>
    <ul>
    <li>id (Required)</li>
    </ul>
    """
    try:
        task = Task.objects.get(id=request.DATA['id'])
        
        task.delete()
        
        return Response({"message": "Task deleted."})
    except (ValueError, MultiValueDictKeyError):
        return Response({"message": "Missing parameter"}, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def edit_task(request):
    """<h3>Edit task.</h3>
    <h4>Headers</h4>
    <ul>
    <li>Authorization (Required, Basic Auth see http://tools.ietf.org/html/rfc2617)</li>
    </ul>
    <h4>Parameters</h4>
    <ul>
    <li>id (Required)</li>
    <li>name (Optional)</li>
    <li>completed (Optional default=False)</li>
    <li>due_date (Optional Date in `yyyy-mm-dd` format)</li>
    <li>priority (Optional default=0; 0 for None, 1 for Important, 2 for Critical)</li>
    </ul>
    """
    try:
        task = Task.objects.get(id=request.DATA['id'])
        
        # Validate input
        
        if request.user != task.created_by:
            return Response({"message": "This task is not belong to you."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            name = request.DATA['name']
            
            if len(name) > 2000:
                return Response({"message": "Task's name must not longer than 2000 characters.", "error_field": "name"}, status=status.HTTP_400_BAD_REQUEST)
            elif len(name) > 0:
                task.name = name
        except:
            pass
        
        try:
            task.completed = request.DATA['completed']
            
            try:
                task.completed = task.completed.lower()
            except:
                pass
            
            if task.completed == True or task.completed == "true" or task.completed == "1":
                task.completed = True
            elif task.completed == False or task.completed == "false" or task.completed == "0":
                task.completed = False
            else:
                return Response({"message": "This field must be boolean (True, False).", "error_field": "completed"}, status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            pass
        
        try:
            task.due_date = request.DATA['due_date']
            datetime.strptime(task.due_date, '%Y-%m-%d')
        except MultiValueDictKeyError:
            task.due_date = None;
        except:
            return Response({"message": "Please enter date in YYYY-MM-DD format.", "error_field":"due_date"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            task.priority = int(request.DATA['priority'])
            
            if task.priority < 0 or task.priority > 2:
                raise ValueError
        except MultiValueDictKeyError:
            pass
        except ValueError:
            return Response({"message": "Priority must be %s." % Task.choices.__str__(), "error_field": "priority"}, status=status.HTTP_400_BAD_REQUEST)
        
        task.save()
        
        return Response({"message": "Task updated", "task": task.to_dict()})
    except MultiValueDictKeyError:
        return Response({"message": "Missing parameter"}, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
