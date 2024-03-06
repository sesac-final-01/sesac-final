from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

# from .models import Lecture
from .serializers import LectureListSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection


class LectureListGetView(APIView):
    serializer_class = LectureListSerializer

    def get(self, request, *args, **kwargs):
        lectures = []

        with connection.cursor() as cursor:
            cursor.execute("select * from Lecture")
            rows = cursor.fetchall()
            for row in rows:
                professor_id = row[1]
                cursor.execute(f"select professor_name from Professor where professor_id={professor_id}")

                lecture_data = {
                    "lec_id": row[0],
                    "professor_name": str(cursor.fetchall()).strip('(''').strip("',)"),
                    "lec_name": row[2],
                    "major": row[3],
                    "lec_level": row[4],
                    "liberal_arts": row[5],
                    "lec_room": row[6],
                    "lec_quota": row[7],
                    "credit": row[8],
                    "lec_schedule": row[9]
                }
                lectures.append(lecture_data)
        serializer = self.serializer_class(instance=lectures, many=True)
        return JsonResponse({"lectures": serializer.data})


class LectureSearchView(APIView):
    serializer_class = LectureListSerializer

    def get(self, request, *args, **kwargs):
        request_code = request.GET.get('lec_id')
        request_name = request.GET.get('lec_name')

        lectures = []
        query = ""
        with connection.cursor() as cursor:
            if request_code and not request_name:
                query = f"select * from Lecture where lec_id={request_code}"
            elif not request_code and request_name:
                query = f"select * from Lecture where lec_name={request_name}"
            elif request_code and request_name:
                query = f"select * from Lecture where lec_id={request_code} and lec_name={request_name}"
            print(query)

            if query:
                cursor.execute(query)
                rows = cursor.fetchall()
                print(f"rows:{rows}")
                if rows:
                    for row in rows:
                        professor_id = row[1]
                        cursor.execute(f"select professor_name from Professor where professor_id={professor_id}")
                        professor_name = str(cursor.fetchone()[0]).strip('(''').strip("',)")

                        print(f"professor_name = {professor_name}")
                        lecture_data = {
                            "lec_id": row[0],
                            "professor_name": professor_name,
                            "lec_name": row[2],
                            "major": row[3],
                            "lec_level": row[4],
                            "liberal_arts": row[5],
                            "lec_room": row[6],
                            "lec_quota": row[7],
                            "credit": row[8],
                            "lec_schedule": row[9]
                        }
                        lectures.append(lecture_data)
                else:
                    return Response("해당 조건에 맞는 수업이 없습니다.")
            else:
                return Response("조건을 입력하지 않았습니다.")
        serializer = self.serializer_class(instance=lectures, many=True)
        return JsonResponse({"searched lectures": serializer.data})