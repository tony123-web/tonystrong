from django.contrib.auth.password_validation import password_changed
from django.forms import  ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User
#from django.contrib.auth.models import User


class myUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password1', 'password2']

class Roomform (ModelForm):
    class Meta:
        model = Room
        fields =  "__all__"
        exclude = ['host', 'participants']


class Userform(ModelForm):
    class Meta:
        model = User
        fields= ['username', 'email', 'avatar', 'bio']
