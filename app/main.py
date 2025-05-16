from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.models.gpt_api import GPTClient
import shutil
import os
import json  # GPT에 JSON 문자열 전달을 위함
import uuid

from app.models.model import analyze_face
from app.models.gpt_api import GPTClient  # ✅ 추가
from app.models.bg_removal.modnet_removal import remove_background_modnet  # ✅ MODNet만 남김
from app.models.bg_removal.bria_rmbg_removal import remove_background_bria_rmbg  # ✅ BRIA RMBG 추가

app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5555"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 제공을 위한 디렉토리 설정
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
    prompt = f"""
    다음은 사용자의 얼굴 사진이 여권 사진의 가이드라인에 적합한지를 분석한 JSON 형식의 결과입니다.
    이 결과를 바탕으로 사진이 적합한지 여부를 판단하고, 사용자에게 이해하기 쉬운 조언을 친절한 말투로 작성해 주세요.

    조건:
    - 전체적인 결과를 바탕으로 사진이 적합한지 알려 주세요.
    - 부적합한 경우, 어떤 점을 개선하면 좋을지 사진 촬영 팁을 알려 주세요.
    - 너무 딱딱하지 않고, 부드럽고 친절한 말투로 작성해 주세요.

    분석 결과:
    {json.dumps(result, ensure_ascii=False, indent=2)}
    """

    # GPT에 프롬프트 전송 및 응답 받기
    response = gpt.ask(prompt, temperature=1.0, max_tokens=256)

    print("gpt_result", response)
    
    # 원본 이미지 삭제
    # if os.path.exists(image_path):
    #     os.remove(image_path)

    # 결과 반환
    return JSONResponse(content={"gpt_result": response, "model_result": result})

# ✅ 배경 제거 API (BRIA RMBG 기본값, modnet만 선택 가능)
@app.post("/api/remove-background")
async def remove_background_api(
    image: UploadFile = File(...),
    method: str = Query("bria", description="배경 제거 방법 ('bria', 'modnet')")
):
    save_dir = "app/static"
    os.makedirs(save_dir, exist_ok=True)

    # 고유한 파일명 생성
    original_filename = image.filename
    file_ext = os.path.splitext(original_filename)[1].lower()
    
    # 알파 채널을 지원하는 PNG 형식으로 출력 파일 확장자 지정
    unique_id = uuid.uuid4().hex
    input_path = os.path.join(save_dir, f"original_{unique_id}{file_ext}")
    output_path = os.path.join(save_dir, f"nobg_{unique_id}.png")  # 항상 PNG로 저장

    # 업로드된 이미지 저장
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    print(f"[DEBUG] 업로드된 이미지가 로컬에 저장됨: {input_path}")

    # 선택한 방법에 따라 배경 제거 함수 호출
    success = False
    method_used = method  # 실제 사용된 방법을 추적
    try:
        if method == "modnet":
            # MODNet 방식 (ONNX 기반)
            try:
                print(f"[DEBUG] MODNet에 전달할 입력 경로: {input_path}")
                success = remove_background_modnet(
                    input_path=input_path,
                    output_path=output_path
                )
            except Exception as e:
                print(f"MODNet 오류: {str(e)}")
                success = False
        else:
            # BRIA RMBG (기본값)
            try:
                remove_background_bria_rmbg(
                    input_path=input_path,
                    output_path=output_path
                )
                success = True
                method_used = "bria"
            except Exception as e:
                print(f"BRIA RMBG 오류: {str(e)}")
                success = False
    except Exception as e:
        print(f"배경 제거 오류: {str(e)}")
        success = False

    # 원본 이미지 삭제
    if os.path.exists(input_path):
        os.remove(input_path)

    if success:
        # 정적 파일 URL 생성
        file_url = f"/static/nobg_{unique_id}.png"
        return JSONResponse(content={
            "success": True,
            "message": "배경이 성공적으로 제거되었습니다.",
            "file_url": file_url,
            "method": method_used
        })
    else:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "배경 제거 처리 중 오류가 발생했습니다."
            }
        )
