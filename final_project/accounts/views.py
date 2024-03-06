from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import *
from rest_framework.generics import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import AllowAny
from django.utils import timezone

class UserSignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        student_id = request.data['student_id']
        # user_id = request.data['user_id']
        password = request.data['password']

        # print(f"student_id={student_id}, user_id={user_id}, password={password}")
        print(f"student_id={student_id}, password={password}")

        user_data = {
            'student_id': student_id,
            # 'user_id': user_id,
            'password': make_password(password)
        }

        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.create(user_data)
            return JsonResponse({"user_num": user.pk, "message": f"student_id - {student_id} user_create success"})
        else:
            print(serializer.errors)
            return Response('user_create failed')


class UserSigninView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

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
                return Response(f"student_id={req_student_id} signin success")
            else:
                return Response(f"wrong password")

        except User.DoesNotExist:
            return Response(f"student_id={req_student_id} user doesn't exist")


class UserSignoutView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        signout_student_id = request.GET.get('student_id')
        # signout_student_id = request.data['student_id']
        print(f"signout_sid={signout_student_id}")
        user = User.objects.get(student_id=signout_student_id)

        if user.logged_in:
            user.logged_in = False
            user.save()
            return Response(f"student_id={signout_student_id} user logged out successfully")
        else:
            return Response(f"student_id={signout_student_id} user already signed out")
