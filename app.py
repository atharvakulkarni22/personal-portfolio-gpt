from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

import os
import streamlit as st

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Load and split resume + cover letter
def load_documents(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=50)
    docs = splitter.split_text(text)
    return [Document(page_content=d) for d in docs]

# Build FAISS vector store
def create_vector_store(documents):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(documents, embeddings)

# Build QA chain
def build_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)
    llm = OpenAI(temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Streamlit app
def main():
    st.title("🤖 Personal Portfolio GPT")

    user_question = st.text_input("Ask about my experience, skills, or background:")
    if user_question:
        docs = load_documents("resume_and_cover_letter.txt")
        vs = create_vector_store(docs)
        qa_chain = build_chain(vs)
        answer = qa_chain.run(user_question)
        st.markdown(f"**Answer:** {answer}")

if __name__ == "__main__":
    main()
