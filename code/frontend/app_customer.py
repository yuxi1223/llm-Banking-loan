import sys 
sys.path.insert(0,"./code")

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
import whisper
import tempfile
import time
import PyPDF2

load_dotenv()
loan="廠房貸款、土地貸款、週轉金貸款、材料貸款"
def chat_with_llm(audio,pdf,style):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI-KEY")
    os.environ["OPENAI_ORGANIZATION"] = os.getenv("OPENAI_ORGANIZATION")
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], 
             openai_organization=os.environ["OPENAI_ORGANIZATION"],
             model=os.getenv("LLM_MODEL"),
             temperature=0,
             streaming=True)
    
    template = """
    # Answer rule
        - It's the generator style ({style}).
        - Let's think step by step.
        - You are a summary bot, helping bank loan officers with summarization tasks.
        - respond using Traditional Chinese (Taiwan), and do not use English.
        - You will have a customer audio text ({audio}) and my notes ({PDF}).
        - The audio text maybe have wrong word ,you need to fix it..
        - You need to summarize the audio text and write a customer requirement report.
        - You need to provide some advice on the mistakes in my notes based on the original audio text.
        - Provide the requirement report text you need to be checked and listed in a markdown table.
        - The table need to have 4 columns.
    """
    prompt = PromptTemplate.from_template(template)
    llm_chain = prompt | llm
    feedback=llm_chain.invoke({'audio':audio,'PDF':pdf,'style':style})
    return(feedback.content)

def chat_with_llm_2(report,loan):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI-KEY")
    os.environ["OPENAI_ORGANIZATION"] = os.getenv("OPENAI_ORGANIZATION")
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], 
             openai_organization=os.environ["OPENAI_ORGANIZATION"],
             model=os.getenv("LLM_MODEL"),
             temperature=0,
             streaming=True)
    
    template = """
    # Answer rule
        - Let's think step by step.
        - You are a loan product bot, helping bankers suggest suitable loan products based on customer reports.
        - respond using Traditional Chinese (Taiwan), and do not use English.
        - You need to base on based on customer reports{report} to find a suitable loan products.{loan}
    """
    prompt = PromptTemplate.from_template(template)
    llm_chain = prompt | llm
    feedback=llm_chain.invoke({'report':report,'loan':loan})
    return(feedback.content)

def audio_to_text(file):
    ear =whisper.load_model(os.getenv("WHISPER_MODEL"))
    customer_text = ear.transcribe(audio=file,
                                   word_timestamps=True,
                                   fp16=False,
    )
    return(customer_text["text"])

def pdf_to_text(file):  
    reader = PyPDF2.PdfReader(file)
    number_of_pages = len(reader.pages)
    text=''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text+= page.extract_text()
    return(text)


st.set_page_config(page_title="客戶需求機器人", page_icon="📖", layout="wide")
st.header("🤖 企業貸款機器人")


with st.sidebar:
    st.markdown(
        "# 🔊 上傳訪談音檔\n"  # noqa: E501
    )
    uploaded_file = st.file_uploader(
        "🔊 Upload a mp3, mp4, or wav file",
        type=["mp3", "m4a",'mp4', "wav"]
    )
   
    

    st.markdown("---")
    st.markdown(
        "# 📄 上傳客戶紀錄\n"  # noqa: E501
    )
    uploaded_file_text = st.file_uploader(
        "📜 Upload a pdf, docx, or txt file",
        type=["pdf", "docx", "txt"]
    )
    


with st.chat_message("assistant"):
    st.markdown("##### 哈囉！！ 我是一位協助您更好了解客戶需求的機器人，並且提供紀錄上的建議 ~"  )

with st.chat_message("assistant"):
    st.markdown("##### 讓我們一起了解客戶，協助他們的需求！！！ ")

if uploaded_file:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())

    with st.chat_message("assistant"):
        audio_text=audio_to_text(path)
        st.markdown("##### 音檔已載入")
        audio=audio_text
else:
    audio=""
        
if uploaded_file_text:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file_text.name)
    with open(path, "wb") as f:
        f.write(uploaded_file_text.getvalue())

    with st.chat_message("assistant"):
        pdf_text=pdf_to_text(path)
        st.markdown("##### 筆記已載入")
        pdf=pdf_text
else:
    pdf=""


user_prompt = st.chat_input("輸入您的紀錄風格")

if user_prompt:
    with st.chat_message("user"):
        st.markdown('##### '+user_prompt)

    with st.spinner("##### 正在為您設計中，請稍等"):
        text=chat_with_llm(audio,pdf,user_prompt)
        with st.chat_message("assistant"):
            st.markdown(text)
        text_2=chat_with_llm_2(text,loan)
        with st.chat_message("assistant"):
            st.markdown(text_2)
        
      