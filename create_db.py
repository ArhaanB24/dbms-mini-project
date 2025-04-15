from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
from time import sleep
import shutil
import os


DATA_PATH = "data/"
CHROMA_PATH = "chroma"
load_dotenv()

api_key = os.getenv("API_KEY")


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf")
    document = loader.load()
    return document
def split_text(documents):
    textsplitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 20,
        length_function = len,
        add_start_index = True
    )
    chunks = textsplitter.split_documents(documents=documents)
    return chunks

def save_to_chroma(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    db = Chroma.from_documents(
        chunks,GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=api_key),persist_directory=CHROMA_PATH
    )

def create_database():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

create_database()
