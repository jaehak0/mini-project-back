# 빌드 스테이지
FROM python:3.10-slim-bullseye as builder

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 최소한의 시스템 패키지만 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libssl-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libopenblas-dev \
    liblapack-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사
COPY requirements.txt .

# 패키지 설치 최적화
RUN pip install --no-cache-dir --no-compile -r requirements.txt \
    && pip install --no-cache-dir --no-compile torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cpu \
    && find /usr/local/lib/python3.10/site-packages -name "*.pyc" -delete \
    && find /usr/local/lib/python3.10/site-packages -name "__pycache__" -delete \
    && find /usr/local/lib/python3.10/site-packages -name "*.so" -exec strip -s {} \; 2>/dev/null || true \
    && find /usr/local/lib/python3.10/site-packages -name "*.c" -delete \
    && find /usr/local/lib/python3.10/site-packages -name "*.pyx" -delete \
    && find /usr/local/lib/python3.10/site-packages -name "*.txt" -delete \
    && rm -rf /root/.cache/pip

# 실행 스테이지 - 더 작은 베이스 이미지 사용
FROM python:3.10-slim-bullseye

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 최소한의 런타임 패키지만 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libssl1.1 \
    libprotobuf23 \
    libopenblas-base \
    liblapack3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# 빌드 스테이지에서 필요한 패키지만 복사
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 애플리케이션 코드 복사 (필요한 파일만)
COPY app/ app/
COPY *.py .

# 환경 변수 설정
ENV PYTHONPATH=/app \
    PATH="/usr/local/bin:${PATH}" \
    PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OPENBLAS_NUM_THREADS=1

# 디렉토리 생성
RUN mkdir -p app/static

# 불필요한 권한 제한 및 사용자 생성 (보안 강화)
RUN addgroup --system app && adduser --system --group app \
    && chown -R app:app /app
USER app

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]