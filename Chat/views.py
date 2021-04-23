from django.contrib.auth import authenticate, login
from Auth.models import User,LastSeen 

from datetime import datetime ,timedelta
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from Chat.models import Message
from Chat.forms import SignUpForm
from Chat.serializers import MessageSerializer, UserSerializer


def index(request):
    if request.user.is_authenticated:
         return redirect( 'Chat:chats')
    if request.method == 'GET':
        return render(request, 'empty_base.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return render(request, 'Chat:chats')



@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



def chat_view(request):
    
    if not request.user.is_authenticated:
        return redirect('Chat:index')
    if request.method == "GET":
        return render(request, 'chat.html',
                      {
                          'users': User.objects.exclude(username=request.user.username)
                      
                      })


def message_view(request, sender, receiver):
        return render(request, "messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


#Ajax online and offline users
def users(request):

    
    # Return offline user
    def off_users():
        offline_user =LastSeen.get_user_offline(timedelta(seconds=180)).exclude(id=request.user.id)# to exclude instanc user
        return offline_user

 
    # Return online user 
    def on_users():
        online_user =LastSeen.get_user_active(timedelta(seconds=180)).exclude(id=request.user.id) # to exclude instanc user
        return online_user

    

    return render(request,'users.html' , {
        'off' :off_users(),
        'on' : on_users(),
    })

# Ajax online and offline users nave 
def users_nav(request):
    
    
    # Return offline user
    def off_users():
        offline_user =LastSeen.get_user_offline(timedelta(seconds=180)).exclude(user=request.user.id) # to exclude instanc user
        return offline_user

 
    # Return online user 
    def on_users():
        online_user =LastSeen.get_user_active(timedelta(seconds=180)).exclude(user=request.user.id) # to exclude instanc user
        return online_user

    

    return render(request,'users_nav.html' , {
        'off' :off_users(),
        'on' : on_users(),
    })

