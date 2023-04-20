from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from chat.forms import RoomForm
from chat.models import Room, RoomLog, MessageLog, RoomMember


def index(request):
    room_qs = Room.objects.all()
    return render(request, "chat/index.html", {
        "room_list": room_qs,
    })


@login_required
def room_new(request):
    if Room.objects.filter(owner=request.user.pk).exists():
        room_pk = Room.objects.get(owner=request.user.pk).pk
        return redirect("chat:room_chat",room_pk)
    elif RoomMember.objects.filter(user=request.user.pk).exists():
        room_pk = RoomMember.objects.get(user=request.user.pk).pk
        return redirect("chat:room_chat",room_pk)
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save(commit=False)
            created_room.owner = request.user
            created_room.save()
            roomlog = RoomLog(owner=request.user, room=created_room.pk, room_name=created_room.name, owner_gender=request.user.gender)
            roomlog.save()
            return redirect("chat:room_chat", created_room.pk)
    else:
        # 정신나갈거같아
        opposite = {'male': 'female', 'female' : 'male'}
        room_log = RoomLog.objects.get(is_full = False and the_other=0 and owner_gender = opposite[request.user.gender])
        room_member = RoomMember(room = room, user = request.user)
        room_member.save()
        room_log = RoomLog.objects.get(room = room.pk)
        room_log.the_other = request.user.pk
        room.save()
        
        return redirect("chat:room_chat",room.pk)

    return render(request, "chat/room_form.html", {
        "form": form,
    })


@login_required
def room_chat(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    return render(request, "chat/room_chat.html", {
        "room": room,
    })


@login_required
def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if room.owner != request.user:
        messages.error(request, "채팅방 소유자가 아닙니다.")
        return redirect("chat:index")

    if request.method == "POST":
        roomlog = RoomLog.objects.get(pk=room_pk)
        roomlog.deleted = 1
        roomlog.save()
        room.delete()
        messages.success(request, "채팅방을 삭제했습니다.")
        return redirect("chat:index")

    return render(request, "chat/room_confirm_delete.html", {
        "room": room,
    })


@login_required
def room_users(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if not room.is_joined_user(request.user):
        return HttpResponse("Unauthorized user", status=401)

    username_list = room.get_online_usernames()

    return JsonResponse({
        "username_list": username_list,
    })
