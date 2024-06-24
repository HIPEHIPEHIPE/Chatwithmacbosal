import os
import fitz  # PyMuPDF
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# PDF 파일 경로 설정
pdf_directory = './pdf'
pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# 모든 PDF 파일의 텍스트 추출
all_texts = ""
for pdf_path in pdf_files:
    pdf_document = fitz.open(pdf_path)
    pdf_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()
    all_texts += pdf_text

# 텍스트 분할
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_text(all_texts)

# texts 리스트가 문자열로만 구성되었는지 확인
texts = [text for text in texts if isinstance(text, str)]

documents = [Document(page_content=text) for text in texts]

# 임베딩 생성
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={'device': 'mps'},  # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
    encode_kwargs={'normalize_embeddings': True},  # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
)

# FAISS 벡터 저장소 생성
vectorstore = FAISS.from_documents(
    documents, 
    embedding=embeddings,
    distance_strategy=DistanceStrategy.COSINE  # 코사인 유사도 측정. 값이 클수록 더 유사함을 의미
)

# 로컬에 DB 저장
MY_FAISS_INDEX = "MY_FAISS_INDEX"
vectorstore.save_local(MY_FAISS_INDEX)

# Chroma 벡터 저장소 경로 설정 및 생성
vectorstore_path = 'vectorstore'
os.makedirs(vectorstore_path, exist_ok=True)

# query_embedding을 호출하기 전에 query가 str 타입인지 확인하는 함수
def ensure_str_query(query):
    if isinstance(query, str):
        return query
    elif isinstance(query, dict):
        # dict에서 필요한 정보를 추출하여 str로 변환
        return query.get("content", "")
    else:
        raise ValueError(f"Unsupported query type: {type(query)}")

# ChromaFixed 클래스 정의
class ChromaFixed(Chroma):
    def similarity_search(self, query, k=3, **kwargs):
        query = ensure_str_query(query)  # query를 str로 변환
        return super().similarity_search(query, k, **kwargs)

    def similarity_search_with_score(self, query, k=3, **kwargs):
        query = ensure_str_query(query)  # query를 str로 변환
        return super().similarity_search_with_score(query, k, **kwargs)

# 수정된 Chroma 벡터 저장소 사용
vectorstore = ChromaFixed.from_documents(documents, embeddings, persist_directory=vectorstore_path)
vectorstore.persist()

# Ollama 를 이용해 로컬에서 LLM 실행
model = ChatOllama(model="eeve:latest", temperature=0, num_gpu=1)
retriever = vectorstore.as_retriever(search_kwargs={'k': 3})

# Prompt 템플릿 생성
template = '''친절한 챗봇으로서 상대방의 요청에 최대한 자세하고 친절하게 답하자. 모든 대답은 한국어로 대답해줘.":
{context}

Question: {question}
'''
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return '\n\n'.join([d.page_content for d in docs])

# RAG Chain 연결
chain = (
    {'context': retriever, 'question': RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
