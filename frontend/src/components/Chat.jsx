import { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Chat({ documentName }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/query`, {
        question: input,
      });

      const aiMessage = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      const errorMessage = {
        role: "assistant",
        content: "Sorry, something went wrong. Please try again.",
        sources: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <p>Chatting with: <strong>{documentName}</strong></p>
      </div>
      <div className="chat-messages">
        {messages.length === 0 && (
          <p className="chat-placeholder">Ask a question about your document...</p>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <p className="message-content">{msg.content}</p>
            {msg.sources && msg.sources.length > 0 && (
              <div className="message-sources">
                <p className="sources-label">Sources:</p>
                {msg.sources.map((source, sIdx) => (
                  <p key={sIdx} className="source-item">{source}</p>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <p className="message-content loading">Thinking...</p>
          </div>
        )}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask a question..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;