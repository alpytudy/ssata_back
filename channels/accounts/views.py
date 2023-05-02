from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

@require_http_methods(["GET", "POST"])
@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('chat:index')
 
    else :
        form = AuthenticationForm()
    context = {'form' : form,}
    return render(request,'accounts/login.html',context)

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('chat:index')

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('chat:index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form, }
    return render(request,'accounts/signup.html',context)

@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('chat:index')
    else:
        form = CustomUserChangeForm()
    context = {'form': form, }
    return render(request,'accounts/update.html',context)

@require_http_methods(["GET", "POST"])
def change_password(request): 
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('chat:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html',context)

@require_POST
def delete(request):
    request.user.delete()   #회원탈퇴
    auth_logout(request)    #로그아웃
    return redirect('chat:index')

# def profile(request, username):  #회원 프로필 구현
#     user = get_user_model().objects.get(username=username)
#     context = {'user': user}
#     return render(request, 'accounts/profile.html', context)


# @require_POST
# def follow(request, user_pk):   #팔로잉 구현
#     if request.user.is_authenticated:     #로그인 됬을경우
#         person = get_user_model().objects.get(pk=user_pk)  #모든 팔로워중에서 요정한 유저pk가 있으면,
#         if request.user in person.followers.all():
#             person.followers.remove(request.user) #제거
#         else:
#             person.followers.add(request.user)  #없으면 생성
#         return redirect('accounts:profile', person.username) #프로필 페이지로 이동, 유저이름데이터를 넘긴다.
#     else:          #미로그인
#         return redirect('accounts:login')

#팔로잉 방법2
# @require_POST
# def follow(request,user_pk):
#     if request.user.is_authenticated:  #로그인 했을때
#         person = get_user_model().objects.get(pk=user_pk)
#         if person != request.user:
#             if person.followers.filter(pk=request.user.pk).exists():  #모든 팔로워중에서 요정한 유저pk가 있으면,
#                 person.followers.remove(request.user)  #제거
#             else:
#                 person.followers.add(request.user)  #없으면 생성

#         return redirect('accounts:profile',person.username)  #프로필 페이지로 이동, 유저이름데이터를 넘긴다.
#     return redirect('accounts:login')    #미로그인 일경우
