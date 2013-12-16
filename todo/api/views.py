from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from todo.api.urls import urlpatterns

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
