# Python code

import streamlit as st
from langserve import RemoteRunnable

st.title('LangChain 기반 영어 번역 애플리케이션')

user_input = st.text_input("영어 문장을 넣어주세요:")

if st.button('전송'):
    remote = RemoteRunnable(url="http://localhost:8000/chat")
    result = remote.invoke({"input": user_input})
    st.write("응답:", result)
