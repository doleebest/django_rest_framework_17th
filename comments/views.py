from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
# Create your views here.

class CommentList(APIView) :
    """
    댓글 생성
    /comment/
    """
    def comment(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    게시물 조회
    /comment/
    """
    def get(self,request, format=None):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

class CommentDetail(APIView) :
    def get_object(self,pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist :
            raise Http404

    """
    특정 게시물 조회
    /comment/{pk}/
    """
    def get(self, request, pk):
        comments = self.get_object(pk)
        serializer = CommentSerializer(comments)
        return Response(serializer.data)

    """
    특정 게시물 수정
    /post/{pk}/
    """
    def put(self, request, pk, format=None):
        comments = self.get_object(pk)
        serializer = Comment(comments, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    특정 게시물 삭제
    /post/{pk}/
    """
    def delete(self,request,pk,format=None):
        comments = self.get_object(pk)
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
