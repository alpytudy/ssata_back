from django.shortcuts import render, redirect,get_object_or_404
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.contrib.auth.decorators import login_required #로그인상태에서만 보이게
# Create your views here.
@require_GET
def index(request): #메인페이지
    articles = Article.objects.all()
    context ={
        'articles':articles
    }
    return render(request, 'articles/index.html',context)

# @login_required    
# @require_GET
def detail(request,pk):  #게시글 세부페이지
    article = Article.objects.get(pk=pk) 

    comment_form =CommentForm()
    comments = article.comment_set.all() 
    context ={
        'article' :article,
        'comment_form':comment_form,
        'comments':comments,
    }
    return render(request, 'articles/detail.html',context)

@login_required    
@require_http_methods(["GET", "POST"])
def create(request): 
    if request.method =='POST':
        form =ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article =form.save(commit=False)  
            article.user =request.user  
            article.save() 
            return redirect('articles:detail',article.pk)
    else:
        form= ArticleForm()
        context = {
            'form' : form
        }
        return render(request, 'articles/create.html',context)
    
@require_http_methods(["GET", "POST"])
def update(request,pk): #게시글 수정
    article = Article.objects.get(pk=pk)
    if request.method =="POST":
        form = ArticleForm(request.POST ,  instance=article)
        if form.is_valid:
            form.save()
            return redirect('articles:detail', article.pk)

    else:
        form = ArticleForm(instance=article)
    context ={
        'article' : article,
        'form' : form
    }
    return render(request, 'articles/update.html',context)

@require_POST
def delete(request,pk):  #게시글 삭제
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


def comments_create(request,pk): #댓글 생성
    if not request.user.is_authenticated:   
        return redirect('accounts:login')  
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article =article
        comment.user = request.user
        comment.save()
    return redirect('articles:detail',article.pk)

def comments_delete(request,article_pk,comment_pk): #댓글 삭제
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail',article_pk)

@require_POST
def likes(request,article_pk): #좋아요 기능
    if request.user.is_authenticated:
        article =Article.objects.get(pk=article_pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect('articles:index')
    return redirect('accounts:login')