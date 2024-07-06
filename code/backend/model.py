
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
import whisper
from langchain_openai import OpenAIEmbeddings
import os

load_dotenv()

def audio_to_text(file_path):
    ear =whisper.load_model(os.getenv("WHISPER_MODEL"))
    customer_text = ear.transcribe(audio=file_path,
                                   word_timestamps=True,
                                   fp16=False,
    )
    return(customer_text["text"])

def chat_with_llm(require):
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI-KEY"), 
             openai_organization=os.getenv("OPENAI_ORGANIZATION"),
             model=os.getenv("LLM_MODEL"),
             temperature=0)
    
    template = """Question: {question}
    # Answer rule
        - Let's think step by step.
        - You are a summary bot, helping bank loan officers with summarization tasks.
        - respond using Traditional Chinese (Taiwan), and do not use English.
    """

    prompt = PromptTemplate.from_template(template)
    llm_chain = prompt | llm
    feedback=llm_chain.invoke(require)
    return(feedback.content)

def embeeding_with_model():
    os.environ["OPENAI_API_KEY"] =os.getenv("OPENAI-KEY")
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_NAME"))
    return(embeddings)

#print(audio_to_text('/Users/yuxisu/Desktop/Su/llm-Banking-loan/loan_data/audio/sfwoy-ky3qe.mp3'))
#print(chat_with_llm("who'r you"))

#text = "This is a test document."
#query_result = embeeding_with_model().embed_query(text)
#print(query_result)