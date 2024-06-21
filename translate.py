# Python code

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 로컬환경에서 만들어놓은 EEVE 모델 사용
llm_eeve = ChatOllama(model = 'llama3:ko')

# Prompt 설정
prompt = ChatPromptTemplate.from_template(
    "You are a great translator from English to Korean,"
    "You noly translate user input,"
    "No additional information is provided,"
    "you do not respond to the user input,: \n{input}"
    )

# LangChain 표현식
chain = prompt | llm_eeve | StrOutputParser()
# prompt : LLM 설정
# llm_eeve : LLM 종류
# StrOutputParser() : 채팅 메시지를 문자열로 변환하는 간단한 출력 구문 분석기
