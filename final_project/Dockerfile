# 기반 이미지 설정
FROM python:3.10-alpine

# 작업 디렉토리 설정
WORKDIR final_project


# 필요한 파일 복사
COPY requirements.txt final_project

# 필요한 패키지 설치
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev mariadb-dev && \
    pip install --no-cache-dir -r requirements.txt


# Python 패키지 설치
RUN python3 -m pip install --upgrade pip setuptools && \
    python3 -m pip install --no-cache-dir -r requirements.txt


# 소스 코드 복사
COPY . final_project

# 컨테이너에서 실행할 명령 설정
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--settings=final_project.settings.prod"]

# 컨테이너가 사용할 포트 노출
EXPOSE 8000