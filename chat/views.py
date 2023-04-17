from django.shortcuts import render,redirect
from .models import Chat_room,Message,Queue_m,Queue_w
from django.db.models import Min, Q
import asyncio, time

# Create your views here.

def lobby(request):
    return render(request, 'chat/lobby.html')

def enter(request, chatroom_pk):
    while not Chat_room.objects.get(pk=chatroom_pk).user2:
        print('waiting')
        print(request.user.username)
        time.sleep(3)
    context = {
        'chatroom_pk': chatroom_pk,
    }
    return render(request, 'chat/chatroom.html', context)

def create(request):
    print('---create---')
    if Chat_room.objects.filter(Q(user1=request.user.pk)|Q(user2=request.user.pk)).exists():
        chatroom=Chat_room.objects.get(Q(user1=request.user.pk)|Q(user2=request.user.pk))
        return redirect('chat:enter',chatroom.pk)
    else:
        if request.user.gender:
            if Queue_w.objects.exists():
                matched=Queue_w.objects.order_by('pk')[0]
                chatroom = Chat_room.objects.get(user1=matched.user.pk)
                chatroom.user2=request.user.pk
                chatroom.save()
                matched.user.waiting=False
                matched.user.save()
                Queue_w.delete(matched)
                return redirect('chat:enter',chatroom.pk)
            else:
                if not request.user.waiting:
                    chatroom = Chat_room(user1=request.user.pk)
                    chatroom.save()
                    waiting=Queue_m(user=request.user)
                    waiting.save()
                    request.user.waiting=True
                    request.user.save()
                    return redirect('chat:enter',chatroom.pk)
                return redirect('chat:lobby')
                
        else:
            if Queue_m.objects.exists():
                matched=Queue_m.objects.order_by('pk')[0]
                chatroom = Chat_room.objects.get(user1=matched.user.pk)
                chatroom.user2=request.user.pk
                chatroom.save()
                matched.user.waiting=False
                matched.user.save()
                Queue_m.delete(matched)
                return redirect('chat:enter',chatroom.pk)
            else:
                if not request.user.waiting:
                    chatroom = Chat_room(user1=request.user.pk)
                    chatroom.save()
                    waiting=Queue_w(user=request.user)
                    waiting.save()
                    request.user.waiting=True
                    request.user.save()
                    return redirect('chat:enter',chatroom.pk)
                return redirect('chat:lobby')
    
def quit(request):
    user=request.user
    if Chat_room.objects.filter(Q(user1=request.user.pk)|Q(user2=request.user.pk)).exists():
        chatroom=Chat_room.objects.get(Q(user1=request.user.pk)|Q(user2=request.user.pk))
        if user.pk==chatroom.user1:
            chatroom.user1=None
            chatroom.save()
        if user.pk==chatroom.user2:
            chatroom.user2=None
            chatroom.save()
        if not chatroom.user1 and not chatroom.user2:
            chatroom.delete()
    return redirect('chat:lobby')
