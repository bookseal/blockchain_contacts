
# 블록체인 튜토리얼

이 튜토리얼은 블록체인 스마트 컨트랙트를 배포하고 Django 웹 애플리케이션을 통해 상호 작용하는 방법을 설명합니다.

## 사전 준비

- Docker
- Docker Compose

## 프로젝트 설정

### 1. 리포지토리 클론

```bash
git clone <repository-url>
cd blockchain_contacts
```

### 2. Docker 이미지를 빌드하고 컨테이너 실행

```bash
docker-compose up --build
```

이 명령어는 Docker 이미지를 빌드하고, Ganache와 Django 웹 애플리케이션 컨테이너를 시작합니다. Ganache가 시작될 때까지 대기한 후 스마트 컨트랙트를 배포하고 Django 개발 서버를 실행합니다.

### 3. Django 웹 애플리케이션에 접속

웹 브라우저에서 다음 URL로 접속합니다:

```
http://localhost:8000
```

## 파일 설명

### Dockerfile

Python 3.9 이미지를 기반으로 하여 필요한 패키지를 설치하고, 프로젝트 파일을 컨테이너로 복사합니다. `entrypoint.sh` 스크립트를 실행하여 Ganache가 시작될 때까지 대기하고 스마트 컨트랙트를 배포한 후 Django 개발 서버를 시작합니다.

### entrypoint.sh

이 스크립트는 Ganache가 시작될 때까지 대기한 후 스마트 컨트랙트를 배포하고 Django 개발 서버를 실행합니다.

### docker-compose.yml

이 파일은 Ganache와 Django 웹 애플리케이션 컨테이너를 정의합니다. 두 서비스는 다음과 같이 설정되어 있습니다:

- `web`: Django 웹 애플리케이션을 실행하는 서비스
- `ganache`: 로컬 이더리움 블록체인 네트워크를 제공하는 Ganache 서비스

### contracts/deploy.py

이 스크립트는 스마트 컨트랙트를 Ganache 네트워크에 배포하고, 배포된 컨트랙트의 주소와 ABI를 `contract_data.json` 파일에 저장합니다.

## 중요 명령어

- 컨테이너 빌드 및 실행: `docker-compose up --build`
- 컨테이너 중지: `docker-compose down`

## 문제 해결

### Ganache가 시작되지 않음

`docker-compose logs ganache` 명령어를 사용하여 Ganache 컨테이너의 로그를 확인합니다.

### 스마트 컨트랙트 배포 실패

`docker-compose logs web` 명령어를 사용하여 Django 웹 애플리케이션 컨테이너의 로그를 확인합니다.

## 기타

이 프로젝트는 학습 목적으로 제공됩니다. 실제 환경에서는 보안과 성능을 고려하여 추가적인 설정이 필요할 수 있습니다.
```

이 `README.md` 파일은 프로젝트를 설정하고 실행하는 방법을 단계별로 설명합니다. 사용자가 쉽게 따라할 수 있도록 각 단계를 명확히 설명했습니다.
