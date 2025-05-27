from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = ["http://localhost:5173"]  # React frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_key

class Query(BaseModel):
    question: str

# Load and process documents
def get_qa_chain():
    with open("resume_and_cover_letter.txt", "r") as f:
        text = f.read()
    chunks = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)
    llm = OpenAI(temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

qa_chain = get_qa_chain()

@app.post("/ask")
def ask_question(query: Query):
    response = qa_chain.run(query.question)
    return {"answer": response}