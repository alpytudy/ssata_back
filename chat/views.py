from django.shortcuts import render
from .models import Chat_room,Message,Queue_m,Queue_w
from django.db.models import Min

# Create your views here.

def lobby(request):
    return render(request, 'chat/lobby.html')


def create(request):
    if request.user.gender:
        if Queue_w.objects.exists():
            matched=Queue_w.objects.get(pk=Min('pk'))
            