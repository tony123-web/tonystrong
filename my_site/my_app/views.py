#from pydoc_data.topics import topics
from wsgiref.util import request_uri
from  django.db.models import Q
#from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import  Room, Topic, Message,User
from .forms import  Roomform, Userform,myUserCreationForm
from django.http import HttpResponse


#rooms = [
 #   {'id': 1, 'name':'Backend developer'},
   # {'id': 2, 'name':'Frontend developer'},
   # {'id': 3, 'name':'Full stack developer'},
 #   {'id': 4, 'name':'Cyber security'},
#]

def loginpage(request):

    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist')

    context = {"page" : page}
    return render(request, "my_app/login_registration.html", context)


def logoutpape(request):
    logout(request)
    return redirect('home')


def registerpage(request):
    form = myUserCreationForm()

    if request.method == "POST":
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registration")
    context = {'form' : form}
    return render(request, 'my_app/login_registration.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
                                )


    topics = Topic.objects.all()[0:3]
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    room_amount = rooms.count()
    context = {'rooms':rooms, 'topics':topics, 'room_message' : room_message,  'room_amount' : room_amount}
    return render(request,"my_app/home.html", context)

def room(request,pk):
    room = Room.objects.get(id = pk)
    participants = room.participants.all()
    messageDetails = room.message_set.all().order_by('-created')

    if request.method == "POST":
        messageInfo = Message.objects.create(
            user=request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'messageDetails': messageDetails, 'participants' : participants}
    return render(request, "my_app/room.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,
               'rooms' : rooms,
               'room_message' : room_message,
               'topics': topics
               }
    return render(request, "my_app/profile.html", context)


@login_required(login_url='login')
def createRoom(request):
    form = Roomform()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name =request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect("home")

       # form = Roomform(request.POST)
        #if form.is_valid():
         #   room = form.save(commit=False)
         #   room.host = request.user
          #  room.save()

    context = {'form' : form , 'topics': topics}
    return render(request, "my_app/room_form.html", context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)

    if request.user != room.host:
        return HttpResponse('This is not your account. You can not Edit')

    if request.method == "POST":
        topics = Topic.objects.all()
        topic = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic)
        room.host = request.user
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect("home")
        #form = Roomform(request.POST, instance=room)
        #if form.is_valid():
           # form.save()

    context = {'form' : form, 'room' : room}
    return render(request, "my_app/room_form.html", context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('This is not your account. You can not delete')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'my_app/delete.html', {'room':room})



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)


    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {"message" : message}
    return render(request, "my_app/deleteMessage.html", context )



@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = Userform(instance=user)

    if request.method == 'POST':
        form = Userform(request.POST,request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    context = {'form': form}
    return render(request,"my_app/update_user.html", context)


def topics_half_screen(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(name__icontains=q)

    return render(request, "my_app/topics_for_half_screen.html", {'topic' : topic})


def activities_half_screen(request):
    room_message = Message.objects.all()
    return render(request, "my_app/activity_half_screen.html", {'room_message' : room_message})



