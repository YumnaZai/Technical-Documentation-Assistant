import { useState } from 'react'

import "./App.css";

//React interacting with the backend
function App() {
  //the memory of the chat app
  const [question, setQuestion] = useState(""); //store the question user typing
  const [messages, setMessages] = useState([]); //stores the messeges/chat history
  const [loading, setLoading] = useState(false); // load response

  const askQuestion = async () => { // this runs when SEND is clicked
    if (!question.trim()) return; //ignore empty input to prevent sending blank messages

    const userMessage = { role: "user", text: question }; //adding user message into chat
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true); //show loading state
    setQuestion("");// clear the input box

    try {
      //send request to backend
      const response = await fetch("http://localhost:8000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage.text }),
      });
      //get the backend answer
      const data = await response.json();

      //adding assistant message
      const assistantMessage = {
        role: "assistant",
        text: data.answer,
        sources: data.sources || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = { //error handling
        role: "assistant",
        text: "Something went wrong reaching the server. Is backend_api.py running?",
        sources: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false); // stop loading
    }
  };
   
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      askQuestion();
    }
  };

  //BUILDING THE UI
  return (
    <div className="app">
      <header className="header"> 
        <h1>Technical Documentation Assistant</h1>
      </header>

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="empty-state">
            Ask a question about the documentation — e.g. "How does
            authentication work?"
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-bubble">
              <p>{msg.text}</p>
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  <span className="sources-label">Sources:</span>
                  {msg.sources.map((src, i) => (
                    <span key={i} className="source-tag">
                      {src}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-bubble loading">Thinking...</div>
          </div>
        )}
      </div>

      <div className="input-bar">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question..."
        />
        <button onClick={askQuestion} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;































