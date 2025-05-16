import onnxruntime as ort
import numpy as np
from PIL import Image
import cv2
import os

def preprocess(img, size=(512, 512)):
    img = img.resize(size, Image.BICUBIC)
    img_np = np.array(img).astype(np.float32) / 255.0
    img_np = (img_np - 0.5) / 0.5  # Normalize to [-1, 1]
    img_np = np.transpose(img_np, (2, 0, 1))  # HWC -> CHW
    img_np = np.expand_dims(img_np, 0)  # Add batch dim
    return img_np

def remove_background_modnet(input_path, output_path):
    """
    ONNX MODNet을 사용하여 배경 제거하는 함수
    """
    model_path = os.path.join(os.path.dirname(__file__), 'weights\\modnet_model.onnx')
    if not os.path.exists(model_path):
        print(f"ONNX MODNet 모델 파일이 없습니다: {model_path}")
        return False
    img = Image.open(input_path).convert('RGB')
    orig_size = img.size
    input_tensor = preprocess(img)
    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    ort_inputs = {session.get_inputs()[0].name: input_tensor}
    ort_outs = session.run(None, ort_inputs)
    matte = ort_outs[0][0, 0]
    matte = np.clip(matte, 0, 1)
    matte = cv2.resize(matte, orig_size, interpolation=cv2.INTER_LINEAR)
    alpha = (matte * 255).astype(np.uint8)
    img_np = np.array(img)
    rgba = np.dstack((img_np, alpha))
    result = Image.fromarray(rgba)
    file_ext = os.path.splitext(output_path)[1].lower()
    if file_ext in ['.jpg', '.jpeg']:
        white_bg = Image.new('RGB', orig_size, (255, 255, 255))
        white_bg.paste(result, mask=result.split()[3])
        result = white_bg
    result.save(output_path)
    return True

if __name__ == "__main__":
    # 예시 경로 (실제 테스트할 파일명으로 수정 가능)
    input_path = "input.jpg"  # 또는 원하는 입력 이미지 경로
    output_path = "output.png"  # 또는 원하는 출력 경로
    remove_background_modnet(input_path, output_path) 