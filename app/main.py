from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models.gpt_api import GPTClient
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
    print("result", result)
    # 기존 GPTClient 인스턴스 생성
    gpt = GPTClient()
    
    # 분석 결과를 GPT에 전송할 프롬프트 생성
    prompt = f"""아래 json형식의 결과는 사용자의 사진이 여권 사진의 가이드라인과 적합한지 여부를 여러 지표를 통해 판단한 결과이다.
    결과를 판단해서 사용자에게 사진에 대한 팁을 알려주는 메세지 작성.
    친절한 말투로 작성하고 이해하기 쉽게 작성.
    어떤 부분에서 적합/부적합인지 설명.
    {json.dumps(result, ensure_ascii=False, indent=2)}"""

    # GPT에 프롬프트 전송 및 응답 받기
    response = gpt.ask(prompt, temperature=1.0, max_tokens=256)

    print("gpt_result", response)
    
    os.remove(image_path)

    # 결과 반환
    return JSONResponse(content={"gpt_result": response, "model_result": result})
