
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Apitest, Comment
from .serializers import ApitestSerializer, CommentSerializer


@api_view(['GET', 'POST'])
def apitest_list(request):
    if request.method == "GET":
        apitests = get_list_or_404(Apitest)
        serializer = ApitestSerializer(apitests, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = ApitestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def apitest_detail(request, apitest_pk):
    apitest = get_object_or_404(Apitest, pk=apitest_pk)

    if request.method == 'GET':
        serializer = ApitestSerializer(apitest)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        apitest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ApitestSerializer(apitest, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET','POST'])
def comment_list(request, apitest_pk):
    apitest = get_list_or_404(apitest, pk=apitest_pk)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(apitest=apitest)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    elif request.method == 'GET':
        comments = Apitest.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def likes(request, apitest_pk):
    if request.user.is_authenticated:
        apitest = get_object_or_404(Apitest, pk=apitest_pk)
        if apitest.like_users.filter(pk=request.user.pk).exist():
            apitest.like_users.remove(request.user)
        else:
            apitest.like_users.add(request.user)
        return redirect('apitest:index')
    return redirect('accounts:login')