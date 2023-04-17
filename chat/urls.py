from django.urls import path 
from . import views 

app_name='chat'
urlpatterns = [
    path('', views.lobby,name='lobby'),
    path('<int:chatroom_pk>/',views.enter,name='enter'),
    path('create/',views.create,name='create'),
    path('quit/',views.quit,name='quit')
]