import sys 
sys.path.insert(0,"./code")

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
from langchain_chroma import Chroma
from backend.model import embeeding_with_model



load_dotenv()

def chat_with_llm(q,docs):
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
        - You are an Answer bot, helping bank loan checker to understand the similarity text{knowledge} base on question{question}.
        - respond using Traditional Chinese (Taiwan), and do not use English.
        - You need to summarize and provide feedback on the important parts of your answer; don't give a long message.
    """

    prompt = PromptTemplate.from_template(template)
    llm_chain = prompt | llm
    feedback=llm_chain.invoke({'question':q,'knowledge':docs})
    return(feedback.content)





st.set_page_config(page_title="授信報告機器人", page_icon="📖", layout="wide")
st.header("🤖 授信報告機器人")


with st.chat_message("assistant"):
    st.markdown("##### 哈囉！！ 我是一位協助你快速閱覽徵信報告的機器人，並且針對你的問題快速回答~"  )

with st.chat_message("assistant"):
    with open('./loan_data/report/loan_report.txt', 'r', encoding='utf-8') as file :
        content = file.read()
        st.markdown(content)

with st.chat_message("assistant"):
    st.markdown("##### 請你詢問任何相關問題！！！ ")


question = st.chat_input("輸入您的問題")
if question:
    with st.chat_message("user"):
        st.markdown("##### "+question)
    with st.spinner("##### 正在為您準備相關訊息，請稍等"):
        embedding_function=embeeding_with_model()
        db = Chroma(persist_directory=os.getenv("CHROMA_PATH"), embedding_function=embedding_function)
        docs=db.similarity_search(question,k=6)
        text=chat_with_llm(question,docs)
        with st.chat_message("assistant"):
            st.markdown(text)
        
            
      