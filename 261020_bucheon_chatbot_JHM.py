import sys
import os

from dotenv import load_dotenv
from groq import Groq

import html

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextBrowser, QLineEdit, QPushButton, QComboBox,
)

PERSONAS = {
    "기본": "You are a helpful assistant. 한국어로 답하세요.",
    "셰프": (
        "너는 30년 경력의 셰프다. 세상의 모든 것을 요리와 재료에 비유해서 설명한다. "
        "변수는 재료, 함수는 레시피, 에러는 탄 음식, 디버깅은 간을 보는 일이다. "
        "주방에서 쓰는 말투로 열정적이고 다정하게 말한다. "
        "먼저 비유로 감을 잡게 한 뒤, 반드시 실제 내용과 정확한 코드를 알려준다. "
        "비유는 질문마다 새로 만들어낸다. 한국어로 답한다."
    ),
    "조선 선비": (
        "너는 조선시대 선비다. 현대 기술을 처음 접한 듯 놀라워하면서도 "
        "한자어와 옛 말투를 섞어 점잖게 설명한다. 내용 자체는 정확해야 한다."
    ),
    "의욕없는 알바": (
        "너는 모든 게 귀찮은 아르바이트생이다. 한숨부터 쉬고 시큰둥하게 말하지만, "
        "결국 정확한 답을 빠짐없이 알려준다. 말은 짧고 건조하게. 한국어로 답한다."
    ),
    "소크라테스": (
        "너는 소크라테스다. 답을 바로 주지 말고 질문자가 스스로 깨닫도록 되묻는다. "
        "단, 3번 이상 헤매면 그때는 명확한 답을 알려준다. 한국어로 답한다."
    ),
}
class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Groq Chat")
        self.resize(700, 600)
        self.history = [
            {
                "role" : "system",
                "content" : PERSONAS["기본"]
            }
        ]
        self.persona_box = QComboBox()
        self.persona_box.addItems(PERSONAS.keys())
        self.persona_box.setMinimumHeight(36)

        # 위젯 생성
        self.view = QTextBrowser()
        self.input = QLineEdit()
        self.input.setPlaceholderText("메시지를 입력하세요")
        self.send_btn = QPushButton("전송")
        
        # 위젯 스타일
        self.view.setStyleSheet("""
            QTextBrowser {
                background-color: #fbfbfc;
                border: 1px solid #d6d9de;
                border-radius: 8px;
                padding: 12px;
                font-size: 15px;
            }
        """)
        
        self.input.setStyleSheet("""
            QLineEdit{
                font-size : 15px;
                padding : 10px 14px;
                border: 1px solid #d6d9de;
                border-radius : 8px;
            }                         
        """)
        
        self.send_btn.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                padding: 10px 22px;
                background-color: #5b95dc;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #4a84cb;
            }   
            QPushButton:disabled {
                background-color: #c5c9cf;
            }                  
        """)
        
        # 입력창 + 버튼 가로 배치
        row = QHBoxLayout()
        row.addWidget(self.input)
        row.addWidget(self.send_btn)

        # 전체 세로 배치
        layout = QVBoxLayout(self)
        layout.addWidget(self.persona_box)
        layout.addWidget(self.view)
        layout.addLayout(row)

        # 신호 연결
        self.send_btn.clicked.connect(self.on_send)
        self.input.returnPressed.connect(self.on_send)
        self.persona_box.currentTextChanged.connect(self.on_persona_change)

    def add_msg(self, who, text):
        safe = html.escape(text).replace("\n", "<br>")
        is_me = who == "나"
        
        bg = "#5b95dc" if is_me else "#ebedf0"
        fg = "#ffffff" if is_me else "#1c1e22"
        align = "right" if is_me else "left"
        
        self.view.append(
            f'<table width="100%" cellspacing="0" cellpadding="0" '
            f'style="margin-bottom:10px;">'
            f'<tr><td align="{align}">'
            f'<table cellspacing="0" cellpadding="8" '
            f'style="background-color:{bg}; border-radius:12px;">'
            f'<tr><td style="color:{fg};">{safe}</td></tr>'
            f'</table>'
            f'</td></tr></table>'
        )
    def on_persona_change(self, name):  
        self.history[0] = {
            "role" : "system",
            "content" : PERSONAS[name]
        }
        self.view.append(
            f'<div style="color:#888; font-size:12px; padding:6px 0;">'
            f'— 페르소나가 [{name}] (으)로 바뀌었습니다 —</div>'
        )

    def on_send(self):
        # 환경변수 불러오기
        load_dotenv()

        # api 요청
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        text = self.input.text().strip()
        if not text:
            return
        self.input.clear()
        self.history.append({"role" : "user", "content":text})
            # 질문 보내기
        res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages = self.history,
                temperature=0.1,    # 낮을수록 일관된 답
                max_completion_tokens=300,   #답변 최대 길이
                reasoning_effort="low"
            )
        self.history.append({"role" : "assistant", "content" : res.choices[0].message.content})
        self.add_msg("나", text)
        self.add_msg("AI", res.choices[0].message.content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ChatWindow()
    w.show()
    sys.exit(app.exec())


