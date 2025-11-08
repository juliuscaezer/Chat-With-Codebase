import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // We'll add this next

function App() {
  const [messages, setMessages] = useState([
    {
        sender: 'bot',
        text: 'Hello! I am ready to answer questions about the LangChain codebase.'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // This is the API URL for our *local test server*
  // We'll update this one last time before we deploy.
  const API_URL = '/api/chat'; 

  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    
    setIsLoading(true);
    setInput(''); 

    try {
      // Send the user's question to our backend API
      const response = await axios.post(API_URL, {
        question: input,
      });

      const botMessage = { sender: 'bot', text: response.data.answer };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

    } catch (error) {
      console.error('Error fetching response from API:', error);
      const errorMessage = { 
        sender: 'bot', 
        text: 'Sorry, I ran into an error. Please try again.' 
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      handleSend();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chat With Your Codebase</h1>
      </header>
      
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
        {isLoading && (
        <div className="message bot">
            <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the repository..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;