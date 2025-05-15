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

