from django.urls import path
from . import views

app_name = 'apitest'

urlpatterns = [
    path('', views.apitest_list, name='index'),
    path('<int:apitest_pk>/', views.apitest_detail),
    path('<int:apitest_pk>/comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('<int:apitest_pk>/likes', views.likes),
]
