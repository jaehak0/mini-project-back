import os  # OS 관련 기능을 사용하기 위한 모듈 임포트
from openai import OpenAI  # OpenAI API를 사용하기 위한 모듈 임포트
from dotenv import load_dotenv  # .env 파일에서 환경변수를 불러오기 위한 모듈 임포트

class GPTClient:  # GPT API를 다루는 클라이언트 클래스 정의
    def __init__(self, model="gpt-3.5-turbo"):  # 클래스 초기화 메서드, 기본 모델은 gpt-3.5-turbo
        # .env 파일에서 환경변수 불러오기
        load_dotenv()  # .env 파일을 읽어서 환경변수로 등록
        self.api_key = os.getenv("OPENAI_API_KEY")  # 환경변수에서 OPENAI_API_KEY 값을 가져옴
        self.client = OpenAI(api_key=self.api_key)  # OpenAI API 클라이언트 객체 생성
        self.model = model  # 사용할 모델 이름 저장

    def ask(self, prompt, temperature=1.0, max_tokens=256):  # 프롬프트를 받아 GPT에게 질문하는 메서드
        try:
            response = self.client.chat.completions.create(  # 챗봇 응답 생성 요청
                model=self.model,  # 사용할 모델 지정
                messages=[
                    {"role": "user", "content": prompt}  # 사용자 메시지로 프롬프트 전달
                ],
                temperature=temperature,  # 창의성(랜덤성) 정도 설정
                max_tokens=max_tokens  # 최대 토큰(응답 길이) 설정
            )
            return response.choices[0].message.content.strip()  # 응답 메시지에서 텍스트만 추출해 반환
        except Exception as e:  # 예외 발생 시
            return f"에러 발생: {e}"  # 에러 메시지 반환