# Python code

import streamlit as st
from langserve import RemoteRunnable

st.title('LangChain_Test')

user_input = st.text_input("질문해주세여:")

if st.button('전송'):
    remote = RemoteRunnable(url="http://localhost:8000/translate")
    result = remote.invoke({"input": user_input})
    st.write("응답:", result)
