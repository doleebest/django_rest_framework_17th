from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework.views import APIView

from .models import User
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status, viewsets
from .serializers import UserSerializer, LoginSerializer
from django_filters import rest_framework as filters, FilterSet
from django.core import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserFilter(FilterSet):
    user = filters.CharFilter(method='filter_user')

    class Meta:
        model = User
        fields = ['username',]

    def filter_user(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

"""
class UserList(APIView):
    def user(self, request, format=None):
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# 로그인을 했는지 안했는지 알아보기위해 홈화면 간단하게 구성
def home(request):
    user_id = request.session.get('username')
    if user_id:
        user = User.objects.get(pk=user_id).first()
        if user:
            return HttpResponse("안녕하세요 %s님" % user)
        else:
            return HttpResponse("프로필이 존재하지 않습니다!")
    else:
        return HttpResponse("로그인 후 이용해주세요!")

def register(request, useremail=None):
    if request.method == 'GET':
        return render(request, 'register.html')


    elif request.method == 'POST':
        username = request.POST.get('username', None)
        #useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        err_data = {}
        if not (username and useremail and password and re_password):
            err_data['error'] = '모든 값을 입력해주세요.'

        elif password != re_password:
            err_data['error'] = '비밀번호가 다릅니다.'

        else:
            user = User(
                username=username,
                useremail=useremail,
                password=make_password(password),
            )
            user.save()
        return render(request, 'register.html', err_data)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    if request.session.filter('user'):
        del (request.session['user'])
    return redirect('/')


class TokenObtainPairSerializer:
    pass


class RegisterSerializer:
    pass

"""
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근해주기
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView):
 serializer_class = LoginSerializer

 def post(self, request, username=None):
     serializer = self.serializer_class(data=request.data)

     if serializer.is_valid(raise_exception=True):
         id = serializer.validated_data['id']
         access = serializer.validated_data['access']
         refresh = serializer.validated_data['refresh']
         #data = serializer.validated_data
         res = Response(
             {
                 "message": "로그인되었습니다.",
                 "id": id,
                 "access": access,
                 "refresh": refresh
             },
             status=status.HTTP_200_OK,
         )
         return res

     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)