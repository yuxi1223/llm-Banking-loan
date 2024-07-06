import sys 
sys.path.insert(0,"./code")

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
from backend.crawler import yahoo_crwaler
import json
import PyPDF2
import tempfile


load_dotenv()

def chat_with_llm(financial,appendices,news,in_data,name):
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
        - List all references used.
        - You are a summary bot, helping bank loan officers with summarization tasks.
        - The summary needs to be in the format of a formal document report.
        - respond using Traditional Chinese (Taiwan), and do not use English.
        - Create a credit report based on the provided data.
        - The report is in a professional style for financial matters.
        - The report should include the following sections:
            (1)企業之組織沿革。
            (2)企業及其主要負責人一般信譽。(summary base on {in_data})
            (3)企業之設備規模概況。
            (4)業務概況。
            (5)存款及授信往來情形。
            (6)保證人一般信譽。
            (7)財務狀況。(summary base on  {financial})
            (8)產業概況(summary base on {news})。

    # Require the Related documents:
            - 徵授信控管流程表、授信案件陳報總行資料明細表(經權以上)
            - 經權以上授信報核書、授信案件往來情形表、授信審議小組會議紀錄
            - 授信關係戶歸戶表、授信戶關係戶確認表
            - 報送主管機關資料、企業用基準利率核算表(非專案)
            - 信保基金申請書、保證書(函)
            - CRM客戶貢獻度、風險性資產收益分析表
            - 營業單位授信報核應自行列入批示條件檢核表
            - 企業授信戶KYC檢核表
            - 企業授信報(審)核檢核表(金管會查核缺失改善事項)
            - 赤道原則適用性檢核表
            - 財務重大變化項目表
            - 企業ESG自評問卷、授信ESG風險程度評估表

    ## You need to check the Related Documents list. If the Related Documents aren't in the appendices, you need to list the missing ones.
    ## Additionally, check the {appendices} basic on Require documents . Also,mention any information that could not be retrieved. Need to lsit the all missing documents.
            
        
    # company name
        - it's the credit report of company {name}
    """

    prompt = PromptTemplate.from_template(template)
    llm_chain = prompt | llm
    feedback=llm_chain.invoke({'financial':financial,'appendices':appendices,'news':news,'in_data':in_data,'name':name})
    return(feedback.content)

def pdf_to_text(file):  
    reader = PyPDF2.PdfReader(file)
    number_of_pages = len(reader.pages)
    text=''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text+= page.extract_text()
    return(text)

st.set_page_config(page_title="徵信報告整理機器人", page_icon="📖", layout="wide")
st.header("🤖 徵信報告機器人")


with st.chat_message("assistant"):
    st.markdown("##### 哈囉！！ 我是一位協助你整理徵信報告的機器人，並且幫你在最後檢查提醒你是否文件有缺漏 ~"  )

with st.chat_message("assistant"):
    st.markdown("##### 讓我們一起製作徵信報告吧！！！ ")
uploaded_file_financial=None
uploaded_file_in_data=None
uploaded_file_appendices=None

with st.sidebar:
    st.markdown(
        "# 1️⃣ 上傳財務資料\n # 2️⃣ 上傳內部資料\n # 3️⃣ 上傳附表\n" 
    )
    uploaded_file = st.file_uploader(
        "📜 Upload a pdf, docx, or txt file",
        type=["pdf", "docx", "txt","json"],
        accept_multiple_files=True
    )

    if uploaded_file:
        if len(uploaded_file)==1:
            uploaded_file_financial=uploaded_file[0]
        elif len(uploaded_file)==2:
            uploaded_file_in_data=uploaded_file[1]
        elif len(uploaded_file)==3:
            uploaded_file_appendices=[2]
    



if uploaded_file_financial!=None:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file_financial.name)
    with open(path, "wb") as f:
        f.write(uploaded_file_financial.getvalue())
    
    with st.chat_message("assistant"):
        st.session_state.financial=pdf_to_text(path)
        with open("./loan_data/report/financial.txt", "w", encoding="utf-8") as file:
            file.write(st.session_state.financial)
        st.write( st.session_state.financial)
        st.markdown("##### 財務報告載入完成")
       
else:
    financial=""

if uploaded_file_in_data!=None:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file_in_data.name)
    with open(path, "wb") as f:
        f.write(uploaded_file_in_data.getvalue())
    
    with st.chat_message("assistant"):
        in_data=pdf_to_text(path)
        with open("./loan_data/report/in_data.txt", "w", encoding="utf-8") as file:
            file.write(in_data)
        st.markdown("##### 內部資料載入完成")
else:
    in_data=""

if uploaded_file_appendices!=None:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir,uploaded_file_appendices.name)
    with open(path, "wb") as f:
        f.write(uploaded_file_appendices.getvalue())
    with st.chat_message("assistant"):
        appendices=pdf_to_text(path)
        st.write("##### 附表載入完成")
else:
    appendices=""

user_prompt = st.chat_input("輸入您的徵信報告公司名稱")
if user_prompt:
    yahoo_crwaler(user_prompt)
    with open(os.getenv('MEWS_PATH'), 'r') as file:
        news = json.load(file)
    with st.chat_message("user"):
        st.markdown("##### "+user_prompt)
    with st.spinner("##### 正在為您統整為一份徵信報告，請稍等"):
        text=chat_with_llm( st.session_state.financial,appendices,news,in_data,user_prompt)
        with st.chat_message("assistant"):
            st.markdown(text)
            with open("./loan_data/report/loan_report.txt", "w", encoding="utf-8") as file:
                file.write(text)
      