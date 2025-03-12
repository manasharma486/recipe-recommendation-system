import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

const ChatBox = ({ messages, onSendMessage, loading }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSendMessage(input);
      setInput('');
    }
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white rounded-xl shadow-lg overflow-hidden chat-container"
    >
      <div className="bg-green-600 text-white p-4">
        <h2 className="text-xl font-semibold flex items-center">
          <i className="fas fa-comment-alt mr-2"></i>
          Ingredient Chat
        </h2>
        <p className="text-sm opacity-80">Tell me what ingredients you have</p>
      </div>
      
      <div className="p-4 chat-messages">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`mb-4 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs md:max-w-md rounded-lg p-3 ${
                message.sender === 'user'
                  ? 'bg-green-500 text-white rounded-br-none'
                  : 'bg-gray-100 text-gray-800 rounded-bl-none'
              }`}
            >
              {message.text}
            </div>
          </motion.div>
        ))}
        
        {loading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-100 text-gray-800 rounded-lg rounded-bl-none p-3">
              <div className="typing-indicator">
                Thinking<span>.</span><span>.</span><span>.</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="List your ingredients (e.g., chicken, rice, tomatoes)"
            className="flex-grow p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            disabled={loading}
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            className="bg-green-600 text-white px-4 py-2 rounded-r-lg disabled:bg-green-400"
            disabled={loading || !input.trim()}
          >
            <i className="fas fa-paper-plane mr-1"></i>
            Send
          </motion.button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          <i className="fas fa-lightbulb text-yellow-500 mr-1"></i>
          Tip: Separate ingredients with commas for better results
        </p>
      </form>
    </motion.div>
  );
};

export default ChatBox; 