from transformers import pipeline
from PIL import Image
import os

def remove_background_bria_rmbg(input_path, output_path):
    # HuggingFace pipeline 로드
    pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)
    # 배경 제거 수행 (Pillow 이미지 반환)
    result_img = pipe(input_path)
    # 결과 저장
    result_img.save(output_path)
    print(f"BRIA RMBG 배경 제거 완료: {output_path}")

if __name__ == "__main__":
    input_path = "input.jpg"
    output_path = "output.png"
    remove_background_bria_rmbg(input_path, output_path) 