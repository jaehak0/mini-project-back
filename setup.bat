@echo off
chcp 65001 > nul

echo ===========================
echo [1] 가상환경 생성 또는 업데이트
echo ===========================

conda env list | findstr "mini-project" > nul
IF %ERRORLEVEL% NEQ 0 (
    echo [!] mini-project 환경이 없어 새로 생성합니다...
    call conda env create -f environment.yml
) ELSE (
    echo [*] mini-project 환경이 이미 존재합니다. 업데이트만 수행합니다...
    call conda env update -f environment.yml
)

echo =========================
echo [2] 백엔드 서버 실행 (FastAPI)
echo =========================
start cmd /k "conda activate mini-project && uvicorn app.main:app --reload --port 8000"

echo =========================
echo [3] 프론트엔드 실행 (React)
echo =========================
start cmd /k "cd /d C:\Users\201-1\Documents\GitHub\mini-project-front && npm install && npm run dev"

echo =========================
echo [4] 웹 브라우저 자동 열기 (React 페이지)
echo =========================
timeout /t 3 > nul
start "" "http://localhost:5555"

echo 🟢 설정 및 서버 시작 완료!
exit /b 0
