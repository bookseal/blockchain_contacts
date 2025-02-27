# Python 3.9 이미지를 기반으로 합니다
FROM python:3.9

# 작업 디렉토리를 설정합니다
WORKDIR /app

# 필요한 시스템 라이브러리 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    cmake \
    libboost-all-dev \
    curl

# 필요한 Python 패키지를 설치합니다
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일을 컨테이너로 복사합니다
COPY . .

# entrypoint.sh 실행 권한 부여
RUN chmod +x /app/entrypoint.sh

# entrypoint.sh 스크립트 실행 및 Django 개발 서버 시작
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
