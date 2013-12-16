from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from todo.api.urls import urlpatterns
from todo.task.models import *

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
    <h4>Parameters</h4>
    <ul>
    <li>Authorization (Required, Basic Auth see http://tools.ietf.org/html/rfc2617)</li>
    </ul>
    """
    try:
        tasks = Task.objects.filter(created_by=request.user).order_by('due_date', 'priority', 'id')
        
        task_dict = []
        
        for task in tasks:
            context = {
                       "id": task.id,
                       "name": u"%s" % task.name,
                       "completed": task.completed,
                       "due_date": task.due_date,
                       "priority": task.priority
                       }
            task_dict.append(context)
        
        return Response({"tasks": task_dict})
    except MultiValueDictKeyError:
        return Response({"message": "Missing parameter"}, status=status.HTTP_400_BAD_REQUEST)
