from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers') #팔로잉 구현
    #(자기자신 상속, 일반적 서비스=맞팔 할필요 없다. , 헷갈리니까 미리 변수명 생성)
    