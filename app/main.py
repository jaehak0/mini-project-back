from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import json  # GPT에 JSON 문자열 전달을 위함


from app.models.model import analyze_face
from app.models.gpt_api import GPTClient  # ✅ 추가

app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5555"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 여권사진 분석 + GPT 결과 API
@app.post("/api/analyze-photo")
async def analyze_photo(image: UploadFile = File(...)):
    save_dir = "app/static"
    os.makedirs(save_dir, exist_ok=True)

    image_path = os.path.join(save_dir, f"temp_{image.filename}")
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # 1. 얼굴 분석
    result = analyze_face(image_path)

    # 2. GPT 응답 생성
    gpt = GPTClient()
    prompt = f"아래 json 형식의 데이터를 파싱 결과를 토대로 여권 사진과 적합한지 여부를 친절히 알려줘.\n{json.dumps(result, ensure_ascii=False)}"
    gpt_response = gpt.ask(prompt)

    # 3. 이미지 삭제
    os.remove(image_path)

    # 4. 결과에 GPT 응답 추가
    result["gpt_result"] = gpt_response
    return JSONResponse(content=result)
