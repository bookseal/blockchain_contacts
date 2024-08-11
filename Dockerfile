# Python 3.9-slim-buster 이미지를 기반으로 합니다
FROM python:3.9-slim-buster

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 라이브러리 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    cmake \
    libboost-all-dev \
    curl \
    postgresql-client \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Python 패키지 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일을 컨테이너로 복사
COPY . /app/

# entrypoint.sh 실행 권한 부여
RUN chmod +x /app/entrypoint.sh

# 앱의 기본 포트를 노출합니다
EXPOSE 8000

# entrypoint.sh 스크립트 실행 및 Django 개발 서버 시작
ENTRYPOINT ["/app/entrypoint.sh"]
