from django.db import models
from django.conf import settings
# from collections import deque

# Create your models here.
class Chat_room(models.Model):
    user1=models.IntegerField()
    user1_quit=models.BooleanField(default=False)
    user2=models.IntegerField()
    user2_quit=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chatroom=models.ForeignKey(Chat_room,on_delete=models.SET_NULL, null=True)
    sender=models.IntegerField()
    sended_at=models.DateTimeField(auto_now_add=True)
    content=models.TextField()

class Queue_m(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Queue_w(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)