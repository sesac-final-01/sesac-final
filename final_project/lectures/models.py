from django.db import models


# class Professor(models.Model):
#     professor_id = models.CharField(max_length=10)
#     professor_name = models.CharField(max_length=10)
#
#
# class Lecture(models.Model):
#     lec_id = models.CharField(max_length=10, null=False)
#     professor = models.ForeignKey("lectures.Professor", related_name="professor",
#                                   on_delete=models.CASCADE, db_column="professor_id")
#     lec_name = models.CharField(max_length=30, null=False)
#     major = models.CharField(max_length=20)
#     lec_level = models.IntegerField(null=False, default=0)
#     liberal_arts = models.BooleanField(default=True)
#     lec_room = models.CharField(max_length=20, null=False)
#     lec_quota = models.IntegerField(null=False)
#     credit = models.IntegerField(null=False, default=3)
#     lec_schedule = models.CharField(max_length=20, null=False)
