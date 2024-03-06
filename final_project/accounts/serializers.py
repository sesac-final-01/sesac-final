from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['student_id', 'password']
        # fields = ['student_id', 'user_id', 'password']


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['student_id', 'password']
