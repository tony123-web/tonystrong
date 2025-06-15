from django.contrib import admin
from  .models import Room
from  .models import Topic
from  .models import User
from  .models import Message

# Register your models here.

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
