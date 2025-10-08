import React from 'react';
import { Chat } from '../types';
import Logo from './Logo';
import '../styles/Sidebar.css';

interface SidebarProps {
  chats: Chat[];
  activeChat: string | null;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ chats, activeChat, onSelectChat, onNewChat }) => {
  const sortedChats = [...chats].sort((a, b) => 
    b.createdAt.getTime() - a.createdAt.getTime()
  );

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <Logo size="large" />
        </div>
        <button className="new-chat-button" onClick={onNewChat}>
          + New Chat
        </button>
      </div>
      <div className="chat-list">
        {sortedChats.length === 0 ? (
          <div className="no-chats">No previous chats</div>
        ) : (
          sortedChats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${chat.id === activeChat ? 'active' : ''}`}
              onClick={() => onSelectChat(chat.id)}
            >
              <div className="chat-title">{chat.title}</div>
              <div className="chat-date">
                {chat.createdAt.toLocaleDateString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Sidebar;