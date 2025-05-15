from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from app.models.model import analyze_face  # ⬅️ 상대 경로로 수정됨

app = FastAPI()

@app.post("/api/analyze-photo")
async def analyze_photo(image: UploadFile = File(...)):
    # 저장 경로를 static/ 폴더로 지정
    save_dir = "app/static"
    os.makedirs(save_dir, exist_ok=True)

    image_path = os.path.join(save_dir, f"temp_{image.filename}")
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # 분석 함수 호출
    result = analyze_face(image_path)

    # 임시 이미지 삭제
    os.remove(image_path)

    return JSONResponse(content=result)
