from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

def get_qa_chain():
    with open("resume_and_cover_letter.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = CharacterTextSplitter(chunk_size=10, chunk_overlap=6).split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-base",
        model_kwargs={"temperature": 0.5, "max_new_tokens": 256}
    )

    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

qa_chain = get_qa_chain()

@app.post("/ask")
def ask_question(query: Query):
    try:
        response = qa_chain.invoke({"query": query.question})
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}