import React, { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatHistory from './components/ChatHistory';
import ChatInput from './components/ChatInput';
import Sidebar from './components/Sidebar';
import { Message, Chat } from './types';
import { sendMessage } from './services/api';
import './App.css';

const App: React.FC = () => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChat, setActiveChat] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Get the current active chat object
  const currentChat = activeChat ? chats.find(chat => chat.id === activeChat) : null;

  // Create a new chat
  const handleNewChat = useCallback(() => {
    const newChatId = uuidv4();
    const newChat: Chat = {
      id: newChatId,
      title: 'New Conversation',
      messages: [],
      createdAt: new Date(),
    };
    
    setChats(prevChats => [...prevChats, newChat]);
    setActiveChat(newChatId);
  }, []);

  // Select an existing chat
  const handleSelectChat = useCallback((chatId: string) => {
    setActiveChat(chatId);
  }, []);

  // Update chat title based on first message
  const updateChatTitle = useCallback((chatId: string, message: string) => {
    setChats(prevChats => 
      prevChats.map(chat => 
        chat.id === chatId 
          ? { 
              ...chat, 
              title: message.length > 30 
                ? `${message.substring(0, 30)}...` 
                : message 
            } 
          : chat
      )
    );
  }, []);

  // Send a message in the current chat
  const handleSendMessage = useCallback(async (text: string) => {
    // If no active chat, create one
    if (!activeChat) {
      handleNewChat();
      return;
    }
    
    // Add user message to chat
    const userMessage: Message = {
      id: uuidv4(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };
    
    // Update the messages in the current chat
    setChats(prevChats => 
      prevChats.map(chat => 
        chat.id === activeChat 
          ? { ...chat, messages: [...chat.messages, userMessage] } 
          : chat
      )
    );
    
    // Update the chat title if this is the first message
    const chat = chats.find(c => c.id === activeChat);
    if (chat && chat.messages.length === 0) {
      updateChatTitle(activeChat, text);
    }
    
    setIsLoading(true);
    
    try {
      // Send message to API
      const response = await sendMessage(text);
      
      // Add bot response to chat
      const botMessage: Message = {
        id: uuidv4(),
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
      };
      
      setChats(prevChats => 
        prevChats.map(chat => 
          chat.id === activeChat 
            ? { ...chat, messages: [...chat.messages, botMessage] } 
            : chat
        )
      );
    } catch (error) {
      console.error('Error in chat:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: uuidv4(),
        text: 'Sorry, there was an error processing your request.',
        sender: 'bot',
        timestamp: new Date(),
      };
      
      setChats(prevChats => 
        prevChats.map(chat => 
          chat.id === activeChat 
            ? { ...chat, messages: [...chat.messages, errorMessage] } 
            : chat
        )
      );
    } finally {
      setIsLoading(false);
    }
  }, [activeChat, chats, handleNewChat, updateChatTitle]);

  return (
    <div className="App">
      <Sidebar 
        chats={chats} 
        activeChat={activeChat} 
        onSelectChat={handleSelectChat} 
        onNewChat={handleNewChat} 
      />
      <div className="main-content">
        {!activeChat ? (
          <div className="empty-state">
            <h2>Welcome to AI Chatbot</h2>
            <p>Start a new conversation by clicking the "New Chat" button.</p>
          </div>
        ) : (
          <div className="chat-container">
            <div className="chat-header">
              {currentChat?.title || 'AI Chatbot'}
            </div>
            <ChatHistory messages={currentChat?.messages || []} />
            {isLoading && (
              <div className="loading-indicator">
                Bot is typing...
              </div>
            )}
            <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;