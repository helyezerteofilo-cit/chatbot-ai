import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatMessage from '../ChatMessage';
import { Message } from '../../types';

// Mock ReactMarkdown to simplify testing
jest.mock('react-markdown', () => {
  return ({ children }: { children: string }) => <div data-testid="markdown">{children}</div>;
});

describe('ChatMessage Component', () => {
  const userMessage: Message = {
    id: '1',
    text: 'Hello, this is a test message',
    sender: 'user',
    timestamp: new Date('2023-05-15T10:30:00'),
  };

  const botMessage: Message = {
    id: '2',
    text: '# Hello\nThis is a *markdown* message',
    sender: 'bot',
    timestamp: new Date('2023-05-15T10:31:00'),
  };

  test('renders user message correctly', () => {
    render(<ChatMessage message={userMessage} />);
    
    // Check message content
    expect(screen.getByText('Hello, this is a test message')).toBeInTheDocument();
    
    // Check message class
    const messageDiv = screen.getByText('Hello, this is a test message').closest('.chat-message');
    expect(messageDiv).toHaveClass('user-message');
    
    // Check timestamp format (will depend on locale settings)
    expect(screen.getByText(/10:30/)).toBeInTheDocument();
  });

  test('renders bot message with markdown', () => {
    render(<ChatMessage message={botMessage} />);
    
    // Check that markdown component is used
    const markdownElement = screen.getByTestId('markdown');
    expect(markdownElement).toBeInTheDocument();
    expect(markdownElement).toHaveTextContent('# Hello This is a *markdown* message');
    
    // Check message class
    const messageDiv = markdownElement.closest('.chat-message');
    expect(messageDiv).toHaveClass('bot-message');
    
    // Check timestamp format
    expect(screen.getByText(/10:31/)).toBeInTheDocument();
  });

  test('renders user message without markdown parsing', () => {
    const userMarkdownMessage = {
      id: '4',
      text: '# This should not be a header',
      sender: 'user' as const,
      timestamp: new Date('2023-10-08T10:33:00')
    };

    render(<ChatMessage message={userMarkdownMessage} />);
    
    // User messages should not parse markdown
    expect(screen.getByText('# This should not be a header')).toBeInTheDocument();
    expect(screen.queryByTestId('markdown')).not.toBeInTheDocument();
  });

  test('handles empty content gracefully', () => {
    const emptyMessage = {
      id: '5',
      text: '',
      sender: 'user' as const,
      timestamp: new Date('2023-10-08T10:34:00')
    };

    render(<ChatMessage message={emptyMessage} />);
    
    const messageDiv = screen.getByText('10:34').closest('.chat-message');
    expect(messageDiv).toBeInTheDocument();
    expect(messageDiv).toHaveClass('user-message');
  });
});