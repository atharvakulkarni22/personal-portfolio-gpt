from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
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

    chunks = CharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", k=5)

    # Better model for improved understanding
    model_id = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=1000,
        temperature=0.2,
        do_sample=True,
        top_p=0.9,
        repetition_penalty=1.1
    )

    llm = HuggingFacePipeline(pipeline=pipe)

    # Custom prompt for better responses
    prompt_template = """Based on the resume and cover letter context below, provide a comprehensive and professional answer to the question.

Context: {context}

Question: {question}

Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )

qa_chain = get_qa_chain()

@app.post("/ask")
def ask_question(query: Query):
    try:
        response = qa_chain.invoke({"query": query.question})
        
        # Extract the result properly
        if isinstance(response, dict) and 'result' in response:
            answer = response['result']
        else:
            answer = str(response)
            
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
