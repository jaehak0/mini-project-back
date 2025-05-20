# 빌드 스테이지
FROM python:3.10-alpine as builder

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    make \
    g++ \
    linux-headers

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 실행 스테이지
FROM python:3.10-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 패키지만 설치
RUN apk add --no-cache \
    libstdc++ \
    libgcc

# 빌드 스테이지에서 설치된 패키지들 복사
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 애플리케이션 코드 복사
COPY . .

# 정적 파일 디렉토리 생성
RUN mkdir -p app/static

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV PATH="/usr/local/bin:${PATH}"
ENV PORT=8000

# 애플리케이션 실행
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} 