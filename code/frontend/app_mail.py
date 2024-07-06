import sys 
sys.path.insert(0,"./code")

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
import json
from backend.crawler import yahoo_crwaler

load_dotenv()

def chat_with_llm(industry,news,case):
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
        - You'r a internal messaging email bot responsible for converting all provided information into email content.
        - respond using Traditional Chinese (Taiwan), and do not use English.
        - You will receive industry updates{industry}, customer news{news}, and corporate loan fraud cases{case}..
        - The email paragraph needs to be divided into three sections: industry updates, customer news, and corporate loan fraud cases, each explained in separate paragraphs.
        - Customer News: This paragraph specifically compiles negative news about customers to raise awareness of companies with negative news.
        - Industry Updates: This paragraph specifically compiles trends in thriving and declining industries to update internal personnel on industry knowledge.
        - Corporate Loan Fraud Cases: This paragraph compiles recent instances of corporate loan fraud at banks to alert internal staff and prevent similar mistakes from occurring.
    """
    prompt = PromptTemplate.from_template(template)
    llm_chain = prompt | llm
    feedback=llm_chain.invoke({'industry':industry,'news':news,'case':case})
    return(feedback.content)

def chat_with_llm_2(news,key):
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
        - You'r a summary news {news} bot.
        - You'll receive news and the search key word {key}.
        - respond using Traditional Chinese (Taiwan), and do not use English.  
    """
    prompt = PromptTemplate.from_template(template)
    llm_chain = prompt | llm
    feedback=llm_chain.invoke({'news':news,'key':key})
    return(feedback.content)



    
st.set_page_config(page_title="郵件機器人", page_icon="📖", layout="wide")
st.header("🤖 郵件機器人")



with st.chat_message("assistant"):
    st.markdown("##### 哈囉！！ 我是你的郵件機器人，協助提供給你客戶負面消息、產業新訊、近期企業貸款詐騙案例 ~"  )

with st.spinner("##### 正在為尋找資料中，請稍等"):
    yahoo_crwaler("公司")
    with open(os.getenv('MEWS_PATH'), 'r') as file:
        news = json.load(file)
    yahoo_crwaler("企業貸款詐欺")
    with open(os.getenv('MEWS_PATH'), 'r') as file:
        case = json.load(file)
    yahoo_crwaler("產業")
    with open(os.getenv('MEWS_PATH'), 'r') as file:
        industry = json.load(file)
    with st.chat_message("assistant"):
        st.markdown("##### 哈囉！！ 我是你的郵件機器人，協助提供給你客戶負面消息、產業新訊、近期企業貸款詐騙案例 ~"  )
        text=chat_with_llm(industry,news,case)

        

user_prompt = st.chat_input("輸入您要詢問的相關新聞")

if user_prompt:
    yahoo_crwaler(user_prompt)
    with open(os.getenv('MEWS_PATH'), 'r') as file:
        news_2 = json.load(file)
    with st.chat_message("user"):
        st.markdown("##### "+user_prompt)
    with st.spinner("##### 正在為您整理中，請稍等"):
        text=chat_with_llm_2(news_2,user_prompt)
        with st.chat_message("assistant"):
            st.markdown(text)
      