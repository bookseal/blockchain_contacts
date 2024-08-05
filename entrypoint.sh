#!/bin/bash
set -e

# Ganache가 실행될 때까지 대기합니다
while ! curl -s http://ganache:8545 > /dev/null; do
  echo "Waiting for Ganache to start..."
  sleep 1
done

echo "Ganache started"

# 컨트랙트 배포 스크립트 실행
python contracts/deploy.py

# Django 개발 서버 실행
exec "$@"
