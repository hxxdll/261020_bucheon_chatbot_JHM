# 261020_bucheon_chatbot_JHM
AI chatbot
# Groq Persona Chatbot

Groq API와 PyQt6로 만든 데스크톱 챗봇입니다.
드롭다운으로 페르소나를 골라 AI의 말투와 성격을 바꿀 수 있습니다.

## 기능

- Groq API를 이용한 대화 (기본 모델: `openai/gpt-oss-20b`)
- 페르소나 5종 선택 — 기본 / 셰프 / 조선 선비 / 의욕없는 알바 / 소크라테스
- 대화 맥락 유지 (이전 질문과 답변을 기억)
- 말풍선 형태의 채팅 UI (내 메시지는 오른쪽, AI는 왼쪽)
- 대화 도중에도 페르소나 변경 가능

## 설치

```bash
git clone https://github.com/hxxdll/261020_bucheon_chatbot_JHM.git
cd 261020_bucheon_chatbot_JHM
pip install -r requirements.txt
```

## API 키 설정

[Groq Console](https://console.groq.com/keys)에서 API 키를 발급받으세요.

`.env.example`을 `.env`로 복사한 뒤 본인의 키를 넣습니다.

```bash
cp .env.example .env
```

```
GROQ_API_KEY=gsk_여기에_본인_키
```

`.env`는 `.gitignore`에 등록되어 있어 저장소에 올라가지 않습니다.

## 실행

```bash
python 261020_bucheon_chatbot_JHM.py
```

창 상단 드롭다운에서 페르소나를 고르고, 아래 입력창에 메시지를 입력한 뒤
Enter 또는 전송 버튼을 누르면 됩니다.

## 페르소나

| 이름 | 설명 |
|------|------|
| 기본 | 일반적인 AI 어시스턴트 |
| 셰프 | 모든 개념을 요리와 재료에 비유해 설명 |
| 조선 선비 | 한자어와 옛 말투를 섞은 점잖은 설명 |
| 의욕없는 알바 | 시큰둥하지만 정확한 답변 |
| 소크라테스 | 답을 주지 않고 되물으며 스스로 깨닫게 유도 |

페르소나를 추가하려면 코드 상단 `PERSONAS` 딕셔너리에 항목을 넣으면 됩니다.
드롭다운에 자동으로 반영됩니다.

```python
PERSONAS = {
    "탐정": "너는 명탐정이다. 모든 질문을 사건으로 취급하며 추리하듯 답한다.",
}
```

## 구조

```
261020_bucheon_chatbot_JHM.py
├── PERSONAS              # 페르소나별 시스템 프롬프트
└── ChatWindow(QWidget)
    ├── __init__          # 위젯 생성, 스타일, 레이아웃, 신호 연결
    ├── add_msg           # HTML 말풍선을 QTextBrowser에 출력
    ├── on_persona_change # history[0]의 시스템 메시지 교체
    └── on_send           # 질문 전송 및 응답 표시
```

대화 기록은 `self.history` 리스트에 쌓이며, 0번 인덱스가 페르소나를 담당하는
시스템 메시지입니다. 페르소나를 바꾸면 이 항목만 교체되고 이전 대화는 유지됩니다.

## 환경

- Python 3.10+
- PyQt6
- groq
- python-dotenv

## 알려진 제한

응답을 받는 동안 창이 잠시 멈춥니다. API 호출이 메인 스레드에서 동기로
실행되기 때문입니다. `QThread`로 분리하면 해결됩니다.
