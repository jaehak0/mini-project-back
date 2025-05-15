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

# 사용 예시
if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 아래 코드 실행
    gpt = GPTClient()  # GPTClient 객체 생성
    question = """아래 json 형식의 데이터를 파싱 결과를 토대로 여권 사진과 적합한지 여부를 친절히 알려줘. {
  "result": "❌ 부적합",
  "emotion": "무표정",
  "입꼬리기울기": -0.0082,
  "입꼬리거리(px)": 223.83,
  "입벌어짐비율": 0,
  "입꼬리비대칭": 1.83,
  "광대비대칭": 10.14,
  "입중앙오프셋": 1.29,
  "눈썹가림": "⭕ 보임",
  "귀노출": "⭕ 보임",
  "시선정면": "⭕ 정면 응시",
  "얼굴정면": "⭕ 정면",
  "최종 판단": "❌ 부적합"
}"""  # 질문 예시
    answer = gpt.ask(question)  # 질문을 GPT에게 보내고 응답 받기
    print("GPT 응답:", answer)  # 응답 출력 