# 💬 Atharva's Portfolio Chatbot GPT

A personalized chatbot built using **LangChain**, **FastAPI**, **React**, and **Hugging Face** that answers questions based on Atharva Kulkarni's resume and cover letter. This AI assistant allows recruiters, collaborators, or visitors to interact with your professional profile in a conversational manner.

---

## 🧠 Features

- RAG (Retrieval-Augmented Generation) architecture using LangChain
- Hugging Face FLAN-T5 model for natural language generation
- Resume + Cover Letter based context using FAISS Vector Store
- Responsive React UI styled with Tailwind CSS
- Real-time interaction via FastAPI backend

---

## 🛠️ Tech Stack

- **Frontend:** React, Tailwind CSS
- **Backend:** FastAPI, LangChain, Hugging Face Transformers
- **LLM:** `google/flan-t5-base` (via Transformers pipeline)
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store:** FAISS
- **Deployment Ready:** Backend can be deployed on Vercel, Render, or any cloud platform

---

## 🚀 Setup & Deployment

### ⚙️ Backend Setup (FastAPI + LangChain)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/personal-portfolio-gpt.git
   cd personal-portfolio-gpt

2. **Install Requirements:**
      ```bash
      pip install -r requirements.txt

4. **Add your resume and cover letter text file.**

5. **Start the backend:**
      ```bash
      uvicorn main:app --host 0.0.0.0 --port 8000 --reload

### 🌐 Frontend Setup (React + Tailwind CSS)
1. **Navigate to the frontend directory:**
      ```bash
      cd ../portfolio-chatbot/

1. **Install dependencies:**
      ```bash
      npm install

3. **Start the development server:**
      ```bash
      npm run dev

4. **Update the backend API URL:**
Inside App.js, replace the axios.post() line with your backend deployment URL if needed:
```bash
const res = await axios.post("https://your-backend-url/ask", { question: input });

