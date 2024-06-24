import streamlit as st
from datetime import datetime
import base64
from Mansae import calculate_bazi
from langserve import RemoteRunnable

# 이미지 파일 로드 및 Base64로 인코딩
image_path = "ICON.png"
with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

image_path2 = "Openimage.png"
with open(image_path2, "rb") as image_file2:
    image_data2 = base64.b64encode(image_file2.read()).decode('utf-8')

# CSS 스타일링 추가
st.markdown("""
    <style>
    .center-content {
        text-align: center;
    }
    .user-message {
        background-color: #007AFF;
        color: white;
        padding: 10px;
        border-radius: 20px;
        margin-bottom: 10px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        float: right;
        clear: both;
    }
    .bot-message {
        background-color: #E5E5EA;
        color: black;
        padding: 10px;
        border-radius: 20px;
        margin-bottom: 10px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        float: left;
        clear: both;
        align-items: center;
    }
    .bot-message img {
        margin-right: 10px;
    }
    .avatar {
        border-radius: 50%;
        width: 30px;
        height: 30px;
    }
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        box-shadow: 0px -2px 5px rgba(0,0,0,0.1);
    }
    .spinner-container {
        position: fixed;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit 앱 제목 및 설명
st.markdown('<h1 class="center-content"> <span style="color:green;">신</span><span style="color:orange;">★</span> <span style="background: linear-gradient(to right, red, orange); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">맥아더보살 무료사주</span><span style="color:orange;">★</span><span style="color:green;">묘</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="center-content"><span style="color:red;">용하다!</span> <span style="color:blue;">용해!</span></h2>', unsafe_allow_html=True)
st.markdown(f'<div class="center-content"><img src="data:image/png;base64,{image_data2}" class="center-image" width="500"></div>', unsafe_allow_html=True)
st.markdown('<p class="center-content">맥아더 보살은 맥아더 장군을 모십니다!!<span style="color:#000;">😎</span></p>', unsafe_allow_html=True)
st.markdown('<p class="center-content">생년월일, 태어난 시간을 알려주시면 운세를 점쳐드립니다!!<span style="color:#000;">🎈</span></p>', unsafe_allow_html=True)
st.markdown('<p class="center-content">보살님이 모시는 맥아더장군은 미국분이기에 영어로 말할 때도 있습니다!!<span style="color:#000;">📢</span></p>', unsafe_allow_html=True)

# 생년월일과 태어난 시간 입력 받기
if 'birth_info_added' not in st.session_state:
    st.session_state.birth_info_added = False

if not st.session_state.birth_info_added:
    st.markdown('<h3 class="center-content">먼저 생년월일과 태어난 시간을 입력해주세요:D</h3>', unsafe_allow_html=True)
    birth_date = st.date_input("생년월일을 선택하세요", value=datetime(1990, 1, 1))
    birth_time = st.time_input("태어난 시각을 입력하세요", value=datetime(1990, 1, 1, 0, 0).time())
    
    if st.button("확인"):
        st.session_state.birth_date = birth_date
        st.session_state.birth_time = birth_time
        st.session_state.birth_info_added = True
        
        # 천간과 지지 계산
        bazi = calculate_bazi(birth_date, birth_time)
        
        # 계산 결과를 session_state에 저장
        st.session_state.bazi = bazi
        
        saju_message = (
            f"입력받은 생년월일: {birth_date}, 태어난 시각: {birth_time}\n"
            f"년간지: {bazi['year_sky']} {bazi['year_ground']}\n"
            f"월간지: {bazi['month_sky']} {bazi['month_ground']}\n"
            f"일간지: {bazi['day_sky']} {bazi['day_ground']}\n"
            f"시간간지: {bazi['hour_sky']} {bazi['hour_ground']}"
        )
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        st.session_state.messages.append({"role": "맥아더보살", "content": saju_message, "type": "system"})

else:
    bazi = st.session_state.bazi
    saju_message = (
        f"입력받은 생년월일: {st.session_state.birth_date}, 태어난 시각: {st.session_state.birth_time}\n"
        f"년간지: {bazi['year_sky']} {bazi['year_ground']}\n"
        f"월간지: {bazi['month_sky']} {bazi['month_ground']}\n"
        f"일간지: {bazi['day_sky']} {bazi['day_ground']}\n"
        f"시간간지: {bazi['hour_sky']} {bazi['hour_ground']}"
    )
    st.markdown(f"<p class='center-content'>{saju_message}</p>", unsafe_allow_html=True)

# 대화 저장을 위한 session_state 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 대화 내용 디스플레이
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message"><img src="data:image/png;base64,{image_data}" class="avatar">{message["content"]}</div>', unsafe_allow_html=True)

# 대화 입력 처리
def clear_question():
    st.session_state.question_input = ""

def handle_question():
    question = st.session_state.question_input
    if question:
        st.session_state.messages.append({"role": "user", "content": question, "type": "human"})
        
        spinner_placeholder = st.empty()
        with spinner_placeholder.container():
            st.markdown('<div class="spinner-container">', unsafe_allow_html=True)
            with st.spinner("답변 생성 중..."):
                remote = RemoteRunnable("http://localhost:8000/chat")
                result = remote.invoke({"messages": [{"role": "user", "content": question, "type": "human"}]})
                
                # result가 딕셔너리 형태인지 확인하고 처리
                if isinstance(result, dict) and "output" in result:
                    output = result["output"]
                else:
                    output = str(result)  # result가 문자열일 경우
                
                st.session_state.messages.append({"role": "맥아더보살", "content": output, "type": "ai"})
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        clear_question()
        spinner_placeholder.empty()

# 입력창 초기화
if 'question_input' not in st.session_state:
    st.session_state.question_input = ""

st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
st.text_input("무엇이 궁금하신가요?", key="question_input", on_change=handle_question)
st.markdown('</div>', unsafe_allow_html=True)
