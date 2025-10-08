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

  // Function to truncate long filenames
  const truncateFilename = (filename: string, maxLength: number = 40) => {
    if (filename.length <= maxLength) return filename;
    
    const extension = filename.split('.').pop();
    const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
    const truncatedName = nameWithoutExt.substring(0, maxLength - extension!.length - 4) + '...';
    
    return `${truncatedName}.${extension}`;
  };

  return (
    <div className={`chat-message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        {/* Show attachments first for user messages */}
        {message.sender === 'user' && message.attachments && message.attachments.length > 0 && (
          <div className="message-attachments">
            {message.attachments.map((attachment) => (
              <div key={attachment.id} className="attachment" title={attachment.name}>
                <span className="attachment-icon">📄</span>
                <span className="attachment-name">
                  {truncateFilename(attachment.name)}
                </span>
              </div>
            ))}
          </div>
        )}
        
        {/* Show text content */}
        {message.text && (
          <div className="message-text">
            {message.sender === 'bot' ? (
              <ReactMarkdown>{message.text}</ReactMarkdown>
            ) : (
              <p>{message.text}</p>
            )}
          </div>
        )}
      </div>
      <div className="message-timestamp">
        {formattedTime}
      </div>
    </div>
  );
};

export default ChatMessage;