from rest_framework.views import APIView

from .models import Lecture, MyLectures, LectureStudents, Professor
from accounts.models import Student

from .serializers import LectureListSerializer, StudentInfoSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection
from django.db.models import Sum
from django.shortcuts import render


class LectureListGetView(APIView):

    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('student_id')
        student = Student.objects.filter(student_id=student_id).values()[0]

        my_lecs_id = LectureStudents.objects.filter(student_id=student_id, canceled=0).values_list('lec_id', flat=True)
        applied_credit = Lecture.objects.filter(pk__in=my_lecs_id).aggregate(credits=Sum('credit'))[
            'credits']  # 신청한 학점 수

        if not applied_credit:
            applied_credit = 0

        student['applied_credit'] = applied_credit

        student_serializer = StudentInfoSerializer(instance=student)

        lectures = Lecture.objects.all().values()
        lectures_res = []
        for lecture in lectures:
            lecture['professor_name'] = Professor.objects.filter(professor_id=lecture['professor_id']).values()[0]['professor_name']
            lectures_res.append(lecture)

        lecture_serializer = LectureListSerializer(instance=lectures_res, many=True)

        # with connection.cursor() as cursor:
        #     cursor.execute("select * from Lecture")
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         professor_id = row[1]
        #         cursor.execute(f"select professor_name from Professor where professor_id={professor_id}")
        #
        #         lecture_data = {
        #             "lec_id": row[0],
        #             "professor_name": str(cursor.fetchall()).strip('(''').strip("',)"),
        #             "lec_name": row[2],
        #             "major": row[3],
        #             "lec_level": row[4],
        #             "liberal_arts": row[5],
        #             "lec_room": row[6],
        #             "lec_quota": row[7],
        #             "credit": row[8],
        #             "lec_schedule": row[9]
        #         }
        #         lectures.append(lecture_data)
        # serializer = self.serializer_class(instance=lectures, many=True)
        # return JsonResponse({"lectures":lecture_serializer.data})
        return JsonResponse({"student":student_serializer.data, "lectures":lecture_serializer.data})


class LectureSearchView(APIView):
    serializer_class = LectureListSerializer

    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('student_id')
        student = Student.objects.filter(student_id=student_id).values()[0]

        my_lecs_id = LectureStudents.objects.filter(student_id=student_id, canceled=0).values_list('lec_id', flat=True)

        applied_credit = Lecture.objects.filter(pk__in=my_lecs_id).aggregate(credits=Sum('credit'))[
            'credits']  # 신청한 학점 수

        if not applied_credit:
            applied_credit = 0

        student['applied_credit'] = applied_credit

        student_serializer = StudentInfoSerializer(instance=student)

        request_code = request.GET.get('lec_id')
        request_name = request.GET.get('lec_name')

        # query = ""
        if request_code and not request_name:
            # query = f"select * from Lecture where lec_id={request_code}"
            lectures = Lecture.objects.filter(lec_id=request_code).values()
        elif not request_code and request_name:
            # query = f"select * from Lecture where lec_name={request_name}"
            lectures = Lecture.objects.filter(lec_name=request_name).values()
        elif request_code and request_name:
            # query = f"select * from Lecture where lec_id={request_code} and lec_name={request_name}"
            lectures = Lecture.objects.filter(lec_id=request_code, lec_name=request_name).values()

        lectures_res = []
        for lecture in lectures:
            lecture['professor_name'] = Professor.objects.filter(professor_id=lecture['professor_id']).values()[0]['professor_name']
            lectures_res.append(lecture)

        lecture_serializer = LectureListSerializer(instance=lectures_res, many=True)

        # with connection.cursor() as cursor::
        # if query:
        #     cursor.execute(query)
        #     rows = cursor.fetchall()
        #     print(f"rows:{rows}")
        #     if rows:
        #         for row in rows:
        #             professor_id = row[1]
        #             cursor.execute(f"select professor_name from Professor where professor_id={professor_id}")
        #             professor_name = str(cursor.fetchall()[0][0]).strip('(''').strip("',)")
        #
        #             print(f"professor_name = {professor_name}")
        #             lecture_data = {
        #                 "lec_id": row[0],
        #                 "professor_name": professor_name,
        #                 "lec_name": row[2],
        #                 "major": row[3],
        #                 "lec_level": row[4],
        #                 "liberal_arts": row[5],
        #                 "lec_room": row[6],
        #                 "lec_quota": row[7],
        #                 "credit": row[8],
        #                 "lec_schedule": row[9]
        #             }
        #             lectures.append(lecture_data)
        #     else:
        #         return Response("해당 조건에 맞는 수업이 없습니다.")
        # else:
        #     return Response("조건을 입력하지 않았습니다.")

        return JsonResponse({"student":student_serializer.data, "lectures": lecture_serializer.data})


class LectureApplyView(APIView):
    def post(self, request, *args, **kwargs):
        request_code = request.data['lec_id']

        # TODO 로그인 시 토큰 발급해 해당 토큰을 통해 student_id 받아올 수 있도록 수정 ; User 생성 시 student_id를 이용한 토큰 발급 必
        student_id = request.data['student_id']

        # with connection.cursor() as cursor:
        #     cursor.execute(f"select * from Lecture where lec_id={request_code}")
        #     lecture = cursor.fetchone()  # 모든 수업은 lec_id가 다름을 가정(같은 수업의 분반인 경우에도)
        #    cursor.execute(f"select * from Student where student_id={student_id}")
        #    student = cursor.fetchone()

        lecture = Lecture.objects.filter(lec_id=request_code).values()[0]
        lec_level = lecture['lec_level']  # 몇 학년 수업인가?
        lec_quota = lecture['lec_quota']  # 수강 정원
        credit = lecture['credit']  # 수강 학점
        lec_schedule = lecture['lec_schedule']  # 수업 시간

        student = Student.objects.filter(student_id=student_id).values()[0]
        student_grade = student['student_grade']
        enroll = student['enroll']
        max_credit = student['max_credit']

        applied_students_count = LectureStudents.objects.filter(lec_id=request_code).count()

        my_lecs_id = LectureStudents.objects.filter(student_id=student_id, canceled=0).values_list('lec_id', flat=True)

        applied_credit = Lecture.objects.filter(pk__in=my_lecs_id).aggregate(credits=Sum('credit'))[
            'credits']  # 신청한 학점 수

        if not applied_credit:
            applied_credit = 0

        applied_schedule = Lecture.objects.filter(pk__in=my_lecs_id).values_list('lec_schedule', flat=True)  # 수업 시간 정보

        # TODO 표준 대기열 SQS 연동
        if enroll:  # 재학생 여부 확인
            if request_code not in my_lecs_id:
                if applied_students_count + 1 <= lec_quota:  # 수강 정원을 초과하지 않은 경우
                    if lec_schedule not in applied_schedule:  # 시간표 중복 여부 확인 - 수강 신청 내역 목록과 비교 必
                        if (applied_credit + credit) <= max_credit:  # 수강 가능 학점 초과 여부 확인
                            LectureStudents.objects.create(
                                # TODO 기존에 신청했다가 취소한 과목 재신청 시  0->1로 바뀌기만 한것들 체크해서 다시 0으로 바꿔주기
                                lec_id=Lecture.objects.get(lec_id=request_code),
                                student_id=Student.objects.get(student_id=student_id))
                            #  TODO 학생 신청 학점 수 증가 必

                            return JsonResponse({"applied_credit": applied_credit+credit, "message":"수강신청 성공"})
                        else:
                            return JsonResponse({"applied_credit": applied_credit, "message": "수강 가능 학점을 초과했습니다"})
                    else:
                        return JsonResponse({"applied_credit": applied_credit, "message": "같은 시간대의 수업을 이미 신청했습니다"})
                else:
                    return JsonResponse({"applied_credit": applied_credit, "message": "수강 정원이 초과되었습니다"})
            else:
                return JsonResponse({"applied_credit": applied_credit, "message": "이미 신청한 강의입니다"})
        else:
            return JsonResponse({"applied_credit": applied_credit, "message": "당학기 수강 신청 대상자가 아닙니다"})


class LectureCancelView(APIView):
    def put(self, request, *args, **kwargs):
        request_code = request.data['lec_id']
        student_id = request.data['student_id']

        delete_lec_info = LectureStudents.objects.get(student_id=student_id, lec_id=request_code, canceled=0)
        print(delete_lec_info)

        if delete_lec_info:
            delete_lec_info.canceled=1
            delete_lec_info.save()

            my_lecs_id = LectureStudents.objects.filter(student_id=student_id, canceled=0).values_list('lec_id', flat=True)
            applied_credit = Lecture.objects.filter(pk__in=my_lecs_id).aggregate(credits=Sum('credit'))[
                'credits']  # 신청한 학점 수

            if not applied_credit:
                applied_credit = 0

            my_lectures = Lecture.objects.filter(pk__in=my_lecs_id).values()
            my_lectures_res = []
            for lecture in my_lectures:
                lecture['professor_name'] = Professor.objects.filter(professor_id=lecture['professor_id']).values()[0][
                    'professor_name']
                my_lectures_res.append(lecture)

            lecture_serializer = LectureListSerializer(instance=my_lectures_res, many=True)

            return JsonResponse({"applied_credit":applied_credit, "my_lectures":lecture_serializer.data})


class MyLectureRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('student_id')
        student = Student.objects.filter(student_id=student_id).values()[0]

        my_lecs_id = LectureStudents.objects.filter(student_id=student_id, canceled=0).values_list('lec_id', flat=True)
        applied_credit = Lecture.objects.filter(pk__in=my_lecs_id).aggregate(credits=Sum('credit'))[
            'credits']  # 신청한 학점 수
        student["applied_credit"] = applied_credit

        student_serializer = StudentInfoSerializer(instance=student)

        my_lectures = Lecture.objects.filter(pk__in=my_lecs_id).values()

        my_lectures_res = []
        for lecture in my_lectures:
            lecture['professor_name'] = Professor.objects.filter(professor_id=lecture['professor_id']).values()[0]['professor_name']
            my_lectures_res.append(lecture)

        lecture_serializer = LectureListSerializer(instance=my_lectures_res, many=True)


        if not applied_credit:
            applied_credit = 0

        return JsonResponse({
            "student":student_serializer.data, "my_lectures": lecture_serializer.data})
