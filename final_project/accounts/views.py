from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from rest_framework.generics import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import  Student


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        student_id = request.data['student_id']
        # user_id = request.data['user_id']
        password = request.data['password']

        try:
            user = User.objects.get(student_id__student_id=student_id)
            return JsonResponse({"status": status.HTTP_208_ALREADY_REPORTED, "message":"해당 학번의 사용자가 이미 존재합니다."})

        except User.DoesNotExist:
            user = User.objects.create(
                student_id=Student.objects.get(student_id=student_id),
                password=make_password(password)
            )
            return JsonResponse({"status": status.HTTP_201_CREATED, "message":"회원가입에 성공했습니다. 로그인 페이지로 이동합니다."})


class UserSigninView(APIView):
    def post(self, request):
        req_student_id = request.data['student_id']
        req_password = request.data['password']

        try:
            user = User.objects.get(student_id=req_student_id)
            user_password = user.password

            if check_password(req_password, user_password):
                user.last_login = timezone.now()
                user.logged_in = True
                user.save()
                return JsonResponse({"status":status.HTTP_200_OK})
            else:
                return JsonResponse({"status":status.HTTP_104_WRONG_PWD})

        except User.DoesNotExist:
            return JsonResponse({"status":status.HTTP_204_NO_CONTENT})


class UserSignoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        signout_student_id = request.GET.get('student_id')
        # signout_student_id = request.data['student_id']
        user = User.objects.get(student_id=signout_student_id)

        if user.logged_in:
            user.logged_in = False
            user.save()
            return Response(f"student_id={signout_student_id} user logged out successfully")
        else:
            return Response(f"student_id={signout_student_id} user already signed out")
