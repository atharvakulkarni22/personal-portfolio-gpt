import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      const res = await axios.post("https://personal-portfolio-gpt-backend.vercel.app/ask", { question: input });
      
      let botResponse;
      if (typeof res.data.answer === 'object' && res.data.answer.result) {
        botResponse = res.data.answer.result;
      } else if (typeof res.data.answer === 'string') {
        botResponse = res.data.answer;
      } else {
        botResponse = JSON.stringify(res.data.answer);
      }
      
      const botMessage = { sender: "bot", text: botResponse };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error("Error:", err);
      const errorMsg = { sender: "bot", text: "Something went wrong. Please try again." };
      setMessages(prev => [...prev, errorMsg]);
    }

    setInput("");
  };

  return (
    <div className="h-screen w-screen bg-gray-900 text-white flex items-center justify-center p-4">
      <div className="w-full max-w-4xl h-full max-h-[90vh] bg-gray-800 rounded-xl shadow-2xl flex flex-col">
        <div className="p-6 border-b border-gray-700">
          <h1 className="text-3xl font-bold text-center">Atharva's Portfolio Chatbot</h1>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-400 text-lg">Ask me anything about the portfolio!</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-xs lg:max-w-md xl:max-w-lg p-3 rounded-lg ${
                  msg.sender === "user" 
                    ? "bg-blue-600 text-white" 
                    : "bg-green-600 text-white"
                }`}>
                  <div className="text-sm font-medium mb-1">
                    {msg.sender === "user" ? "You" : "Portfolio GPT"}
                  </div>
                  <div className="break-words">{msg.text}</div>
                </div>
              </div>
            ))
          )}
        </div>
        
        <div className="p-4 border-t border-gray-700">
          <div className="flex gap-3">
            <input
              type="text"
              className="flex-1 p-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Ask something about the portfolio..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-colors font-medium"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
