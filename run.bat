@echo off
chcp 65001 > nul

echo =========================
echo [1] 백엔드 서버 실행 (FastAPI)
echo =========================
cd /d C:\Users\201-1\mini-project-back
start cmd /k "conda activate mini-project && uvicorn app.main:app --reload --port 8000"

echo =========================
echo [2] 프론트엔드 실행 (React)
echo =========================
start cmd /k "cd /d C:\Users\201-1\Documents\GitHub\mini-project-front && npm run dev"

echo =========================
echo [3] 웹 브라우저 자동 열기 (React 페이지)
echo =========================
start http://localhost:5555