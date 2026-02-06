import React, { useState, useRef, useEffect } from 'react';
import './TaskieChat.css';

const TaskieChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentTasks, setCurrentTasks] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();

    // Initialize with welcome message
    if (messages.length === 0) {
      setMessages([{
        sender: 'taskie',
        text: "Hey there! I'm Taskie, your friendly task assistant! 😊 I can help you add, view, update, complete, or delete tasks. Just tell me what you'd like to do!",
        timestamp: new Date()
      }]);
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = { sender: 'user', text: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Fetch current tasks from localStorage or API (simulated here)
      // In a real app, you would fetch from your API
      const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');

      // Send message to the backend API with current tasks
      const response = await fetch('/chat/public', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          current_tasks: tasks,
          user_id: 'demo_user'  // Using a demo user ID for testing
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add bot response to the chat
      const botMessage = {
        sender: 'taskie',
        text: data.reply || data.response || data.message || 'Sorry, I didn\'t understand that.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);

      // Update tasks if the response contains updated tasks
      if (data.updated_tasks) {
        setCurrentTasks(data.updated_tasks);
        // In a real app, you would update your global state or API
        localStorage.setItem('tasks', JSON.stringify(data.updated_tasks));
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        sender: 'taskie',
        text: 'Sorry, I\'m having trouble connecting. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="taskie-chat-container">
      <div className="taskie-chat-header">
        <h2>Taskie Assistant</h2>
      </div>

      <div className="taskie-chat-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`taskie-message ${msg.sender === 'user' ? 'taskie-user-message' : 'taskie-bot-message'}`}
          >
            <div className="taskie-message-content">
              {msg.text}
            </div>
            <div className="taskie-message-timestamp">
              {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="taskie-message taskie-bot-message">
            <div className="taskie-typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="taskie-chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          disabled={isLoading}
          className="taskie-chat-input"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="taskie-send-button"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default TaskieChat;