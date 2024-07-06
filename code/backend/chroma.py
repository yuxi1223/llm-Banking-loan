from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from model import embeeding_with_model
from dotenv import load_dotenv
import os
import shutil

load_dotenv()
def create_chroma(path):
    embedding_function=embeeding_with_model()
    loader = TextLoader(path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    db = Chroma.from_documents(docs,embedding_function,persist_directory=os.getenv("CHROMA_PATH"))



def load_chroma():
    embedding_function=embeeding_with_model()
    db = Chroma(persist_directory=os.getenv("CHROMA_PATH"), embedding_function=embedding_function)
    return(db)

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"The folder '{folder_path}' has been deleted.")
    else:
        print(f"The folder '{folder_path}' does not exist.")
#delete_folder("./loan_data/chroma/chroma_db")
#create_chroma("./loan_data/report/customer.txt")
#create_chroma("./loan_data/report/loan_report.txt")
#create_chroma("./loan_data/report/in_data.txt")
#create_chroma("./loan_data/report/financial.txt")
