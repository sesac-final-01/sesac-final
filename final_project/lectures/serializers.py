from rest_framework  import serializers
# from .models import  Lecture


class StudentInfoSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=10)
    student_name = serializers.CharField(max_length=20)
    student_grade = serializers.IntegerField()
    major = serializers.CharField(max_length=20)
    max_credit = serializers.IntegerField()
    applied_credit= serializers.IntegerField()


class LectureListSerializer(serializers.Serializer):
    lec_id = serializers.CharField(max_length=10)
    professor_name = serializers.CharField(max_length=10)
    lec_name = serializers.CharField(max_length=30)
    major = serializers.CharField(max_length=20)
    lec_level = serializers.IntegerField()
    liberal_arts = serializers.BooleanField()
    lec_room = serializers.CharField(max_length=20)
    lec_quota = serializers.IntegerField()
    credit = serializers.IntegerField()
    lec_schedule = serializers.CharField(max_length=20)


class LectureApplySerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=10)
    lec_id = serializers.CharField(max_length=10)
    is_active = serializers.BooleanField(default=True)
