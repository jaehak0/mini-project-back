from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.models.model import analyze_face

app = FastAPI()

# ✅ CORS 설정 - 프론트 포트 5555 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5555"],  # 프론트 도메인 명시
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 여권사진 분석 API
@app.post("/api/analyze-photo")
async def analyze_photo(image: UploadFile = File(...)):
    save_dir = "app/static"
    os.makedirs(save_dir, exist_ok=True)

    image_path = os.path.join(save_dir, f"temp_{image.filename}")
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result = analyze_face(image_path)

    os.remove(image_path)
    return JSONResponse(content=result)
