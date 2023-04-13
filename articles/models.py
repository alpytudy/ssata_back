from django.db import models
from django.conf import settings
# 게시판 모델
class Article(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #유저정보 받아오기
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles') # 좋아요 기능
    title = models.CharField(max_length=20)         #제목
    image = models.ImageField(blank=True, null=True)  #이미지 첨부
    created_at = models.DateTimeField(auto_now_add=True)  #생성날짜
    updated_at = models.DateTimeField(auto_now=True)   #수정날짜
    description = models.TextField()     #내용

    def __str__(self):
            return f'{self.id}번째글 - {self.title}'

# 댓글 모델
class Comment(models.Model):  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content =models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    