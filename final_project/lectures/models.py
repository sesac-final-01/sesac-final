from django.db import models


class Professor(models.Model):
    professor_id = models.CharField(max_length=10, null=False, primary_key=True)
    professor_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'Professor'


class Lecture(models.Model):
    lec_id = models.CharField(max_length=10, null=False, primary_key=True)
    professor = models.ForeignKey("Professor", on_delete=models.CASCADE, db_column="professor_id")
    lec_name = models.CharField(max_length=30, null=False)
    major = models.CharField(max_length=20)
    lec_level = models.IntegerField(null=False, default=0)
    liberal_arts = models.BooleanField(default=True)
    lec_room = models.CharField(max_length=20, null=False)
    lec_quota = models.IntegerField(null=False)
    credit = models.IntegerField(null=False, default=3)
    lec_schedule = models.CharField(max_length=20, null=False)

    class Meta:
        managed = False
        db_table = 'Lecture'


class MyLectures(models.Model):
    student_id = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, db_column='student_id')
    lec_id = models.ForeignKey('Lecture', on_delete=models.RESTRICT, db_column='lec_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "MyLectures"


class LectureStudents(models.Model):
    lec_id = models.ForeignKey('Lecture', on_delete=models.RESTRICT, db_column='lec_id')
    student_id = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, db_column='student_id')
    canceled = models.BooleanField(default=False)

    class Meta:
        db_table = "LectureStudents"
