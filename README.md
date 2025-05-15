# 🛂 여권의 정석

**당신의 사진이 여권 사진에 적합한 사진인지 집에서 간단하게 확인해드립니다.**

---

## 📖 개요

"여권의 정석"은 사용자가 업로드한 얼굴 사진을 분석하여,  
해당 사진이 여권용으로 적합한지 다양한 기준에 따라 자동 판단해주는 AI 기반 진단 서비스입니다.

---

## ✨ 주요 기능

1. 사진 업로드 및 분석 요청
2. 감정 분석 (무표정, 행복, 놀람 등)
3. 입꼬리 기울기 계산
4. 입 크기 및 벌어짐 계산
5. 입꼬리 비대칭 측정
6. 광대 비대칭 측정
7. 입 중심 오프셋 계산
8. 눈썹 노출 여부 판단
9. 귀 노출 여부 판단
10. 시선 방향 판단
11. 얼굴 방향 판단
12. 최종 적합성 판단 (통합 평가)
13. 결과 JSON 반환

---

## 🛠️ 기술 스택

| 항목 | 사용 기술 |
|------|------------|
| Frontend | React |
| Backend | FastAPI |
| LLM 연동 | OpenAI GPT API |
| 이미지 분석 | Mediapipe, DeepFace |
| 결과 처리 | Python + JSON 응답 |

---

## ⚙️ 설치 및 실행 방법 (Windows 기준)

```bash
# 📦 GitHub에서 프로젝트 클론
git clone https://github.com/yourteam/your-repo.git  # 👉 실제 팀 GitHub 주소로 바꿔주세요
cd your-repo

# 🛠️ Conda 가상환경 생성 및 활성화 (최초 1회)
conda env create -f environment.yml
conda activate mini-project

# 🔁 이미 가상환경이 존재할 경우 (기존 환경 삭제 후 재생성)
# conda deactivate
# conda remove -n mini-project --all
# conda env create -f environment.yml
# conda activate mini-project

# 💡 혹시 environment.yml로 설치 안 될 경우, 필요한 패키지를 수동 설치하세요
# conda activate mini-project
# pip install fastapi uvicorn python-multipart
# pip install openai python-dotenv

# 🚀 서버 실행
uvicorn app.main:app --reload
```

---

## 👥 팀 소개

**1조**  
- 프로젝트명: **여권의 정석**
- 팀원 수: 5명
- 역할 분담: 프론트엔드, 백엔드, AI 분석, 디자인, 발표 등

---

## 📌 참고

- 본 프로젝트는 졸업작품/학습용으로 제작되었으며, 상업적 용도가 아닙니다.
