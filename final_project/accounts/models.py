from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=10, null=False, primary_key=True)
    student_name = models.CharField(max_length=20)
    student_grade = models.IntegerField(null=False, default=1)
    major = models.CharField(max_length=20, null=False)
    enroll = models.BooleanField(default=True)
    max_credit = models.IntegerField(null=False, default=18)

    class Meta:
        managed = False
        db_table = "Student"


class UserManager(BaseUserManager):
    use_in_migrations = True

    # def create_user(self, student_id, user_id, password):
    def create_user(self, student_id, password):
        if not student_id:
            raise ValueError('Users must enter your student_id')

        user = self.model(
            student_id=student_id,
            # user_id=user_id
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password):
        user = self.create_user(
            student_id=student_id,
            # user_id=user_id,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    student_id = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='student_id', unique=True)
    logged_in = models.BooleanField(default=False)

    # user_id = models.CharField(
    #     max_length=20,
    #     null=False
    # )

    #  중복 로그인 방지(보류)
    # last_login = models.DateTimeField(auto_now=True)  # 로그인 이력 변경 시 간 기록
    # last_ip_addr = models.CharField

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'student_id'

    # REQUIRED_FIELDS = ['user_id']

    class Meta:
        db_table = "User"
