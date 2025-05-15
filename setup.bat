@echo off
chcp 65001 > nul

echo ===========================
echo [1] 기존 가상환경 삭제
echo ===========================
call conda deactivate
call conda remove -n mini-project --all -y

echo ===========================
echo [2] 가상환경 새로 생성
echo ===========================
call conda env create -f environment.yml

echo =========================
echo [3] 백엔드 서버 실행 (FastAPI)
echo =========================
start cmd /k "conda activate mini-project && uvicorn app.main:app --reload --port 8000"

echo =========================
echo [4] 프론트엔드 실행 (React)
echo =========================
start cmd /k "cd /d C:\Users\201-1\Documents\GitHub\mini-project-front && npm run dev"

echo =========================
echo [5] 웹 브라우저 자동 열기 (React 페이지)
echo =========================
start http://localhost:5555