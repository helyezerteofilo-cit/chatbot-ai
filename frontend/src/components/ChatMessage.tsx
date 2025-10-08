import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../types';
import '../styles/ChatMessage.css';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const formattedTime = message.timestamp.toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  return (
    <div className={`chat-message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        {message.sender === 'bot' ? (
          <ReactMarkdown>{message.text}</ReactMarkdown>
        ) : (
          <p>{message.text}</p>
        )}
      </div>
      <div className="message-timestamp">
        {formattedTime}
      </div>
    </div>
  );
};

export default ChatMessage;