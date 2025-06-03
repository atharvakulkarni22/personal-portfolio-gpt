import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      const res = await axios.post("http://localhost:8000/ask", { question: input });
      
      // Handle nested response structure
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
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <div className="max-w-2xl mx-auto bg-gray-800 rounded-xl shadow-lg p-4">
        <h1 className="text-2xl font-bold mb-4">🧑‍💼 Portfolio GPT Chat</h1>
        <div className="h-96 overflow-y-auto flex flex-col gap-2 border border-gray-700 p-2 rounded">
          {messages.map((msg, idx) => (
            <div key={idx} className={`p-2 rounded-lg max-w-xs ${
              msg.sender === "user" 
                ? "bg-blue-500 self-end ml-auto" 
                : "bg-green-600 self-start mr-auto"
            }`}>
              {msg.text}
            </div>
          ))}
        </div>
        <div className="flex gap-2 mt-4">
          <input
            type="text"
            className="flex-1 p-2 rounded bg-gray-700 border border-gray-600 text-white"
            placeholder="Ask something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={handleSend}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded transition-colors"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;