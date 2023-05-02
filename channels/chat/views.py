from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from chat.forms import RoomForm
from chat.models import Room, RoomLog, RoomMember


def index(request):
    room_qs = Room.objects.all()
    return render(request, "chat/index.html", {
        "room_list": room_qs,
    })


@login_required
def room_new(request):  #랜덤매칭
    if Room.objects.filter(owner=request.user.pk).exists():
        room_pk = Room.objects.get(owner=request.user.pk).pk
        room_log = RoomLog.objects.get(room=room_pk)
        if room_log.owner > 0: # 내가 방장(owner)인 방이 있다면, 내 방 재입장
            return redirect("chat:room_chat",room_pk)
    elif RoomLog.objects.filter(deleted=0, the_other=request.user.pk).exists():
        room_log = RoomLog.objects.get(deleted=0, the_other=request.user.pk)
        # room_log = RoomLog.objects.get(room=room_pk)
        # if room_log.the_other > 0:  # 내가 참여자(the_other)인 방이 있다면, 내 방 재입장
        return redirect("chat:room_chat",room_log.room)
    opposite = {'male': 'female', 'female' : 'male'}
    if RoomLog.objects.filter(deleted=0, the_other=0, owner_gender = opposite[request.user.gender]).exists():
        room_log = RoomLog.objects.filter(deleted=0, the_other=0, owner_gender = opposite[request.user.gender])[0]
        room = Room.objects.get(pk=room_log.room)
        room_member = RoomMember(room = room, user = request.user)
        room_member.save()
        room_log.the_other = request.user.pk
        room_log.save()
        return redirect("chat:room_chat",room.pk)
    else:
        # , name=str(RoomLog.objects.count())
        # print(str(RoomLog.objects.count()))
        created_room = Room.objects.create(owner = request.user)
        # created_room.owner = request.user
        created_room.save()
        roomlog = RoomLog(owner=request.user.pk, owner_gender=request.user.gender, room=created_room.pk)
        roomlog.save()  # RoomLog 별도 DB 저장
        return redirect("chat:room_chat", created_room.pk)
        return redirect("chat:index")
    # if request.method == "POST":  # 매칭 요청시  
    #     form = RoomForm(request.POST, name=str(RoomLog.objects.count()))
    #     if form.is_valid():
    #         created_room = form.save(commit=False)
    #         created_room.owner = request.user
    #         created_room.save()
    #         roomlog = RoomLog(owner=request.user.pk, owner_gender=request.user.gender, room=created_room.pk)
    #         roomlog.save()  # RoomLog 별도 DB 저장
    #         return redirect("chat:room_chat", created_room.pk)
    # else:  # 
    #     opposite = {'male': 'female', 'female' : 'male'}
    #     if RoomLog.objects.filter(the_other=0, owner_gender = opposite[request.user.gender]).exists():
    #         room_log = RoomLog.objects.filter(the_other=0, owner_gender = opposite[request.user.gender])[0]
    #         room = Room.objects.get(pk=room_log.room)
    #         room_member = RoomMember(room = room, user = request.user)
    #         room_member.save()
    #         room_log.the_other = request.user.pk
    #         room_log.save()
    #         return redirect("chat:room_chat",room.pk)
    # form = RoomForm()

    # return render(request, "chat/room_form.html", {
    #     "form": form,
    # })


@login_required
def room_chat(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    room_log = get_object_or_404(RoomLog, room=room_pk)
    if request.user.pk not in {room_log.owner, room_log.the_other} or room_log.deleted == 1:
        return redirect("chat:index")
    return render(request, "chat/room_chat.html", {
        "room": room,
    })


# @login_required
# def room_delete(request, room_pk):
#     room = get_object_or_404(Room, pk=room_pk)

#     if room.owner != request.user:
#         messages.error(request, "채팅방 소유자가 아닙니다.")
#         return redirect("chat:index")

#     if request.method == "POST":
#         roomlog = RoomLog.objects.get(room=room_pk)  # RoomLog의 room = Room의 pk
#         roomlog.deleted = 1  # RoomLog 삭제 처리
#         roomlog.save()
#         room.delete()
#         messages.success(request, "채팅방을 삭제했습니다.")
#         return redirect("chat:index")

#     return render(request, "chat/room_confirm_delete.html", {
#         "room": room,
#     })

@login_required
def room_delete(request, room_pk):  # 채팅방 나가기, 삭제, 쫑난방 표기
    room = get_object_or_404(Room, pk=room_pk)
    # (채팅방나가기) 일단 삭제요청오면 (쫑난방 표기)request.user -1처리   + 상대방이 나갔습니다.
    # (채팅방 삭제)그다음에 둘다 -1인지 검사
    # 둘 다 -1이면 삭제
    room_log = get_object_or_404(RoomLog, room=room_pk)
    if request.method == "POST":   #나가기를 눌렀을시
        # room_log = get_object_or_404(RoomLog, room=room_pk)
        if room.owner == request.user:  #나갈사람이 방장인지 아닌지 구분
            room_log.owner = -1
        else:
            room_log.the_other = -1
        messages.success(request, "채팅방을 나갔습니다.")
    if room_log.owner + room_log.the_other == -2 or (room_log.owner ==-1 and room_log.the_other == 0):
        room_log.deleted = 1  # RoomLog 삭제처리
        room_log.save()
        room.delete()      # 진짜 Room 삭제

    #("나가시겠습니까" 확인버튼 추후 제작)    
    return redirect("chat:index")

    





@login_required
def room_users(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if not room.is_joined_user(request.user):
        return HttpResponse("Unauthorized user", status=401)

    username_list = room.get_online_usernames()

    return JsonResponse({
        "username_list": username_list,
    })
