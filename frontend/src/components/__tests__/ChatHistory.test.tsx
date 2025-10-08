import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatHistory from '../ChatHistory';
import { Message } from '../../types';

// Mock the ChatMessage component
jest.mock('../ChatMessage', () => {
  return {
    __esModule: true,
    default: ({ message }: { message: Message }) => (
      <div data-testid="chat-message" data-message-id={message.id} data-sender={message.sender}>
        {message.text}
      </div>
    ),
  };
});

describe('ChatHistory Component', () => {
  const mockMessages: Message[] = [
    {
      id: '1',
      text: 'Hello',
      sender: 'user',
      timestamp: new Date('2023-05-15T10:30:00'),
    },
    {
      id: '2',
      text: 'Hi there!',
      sender: 'bot',
      timestamp: new Date('2023-05-15T10:31:00'),
    },
    {
      id: '3',
      text: 'How are you?',
      sender: 'user',
      timestamp: new Date('2023-05-15T10:32:00'),
    },
  ];

  test('renders empty state when no messages', () => {
    render(<ChatHistory messages={[]} />);
    
    expect(screen.getByText('No messages yet. Start a conversation!')).toBeInTheDocument();
  });

  test('renders all messages in the correct order', () => {
    render(<ChatHistory messages={mockMessages} />);
    
    const messageElements = screen.getAllByTestId('chat-message');
    expect(messageElements).toHaveLength(3);
    
    // Check order and content
    expect(messageElements[0]).toHaveTextContent('Hello');
    expect(messageElements[1]).toHaveTextContent('Hi there!');
    expect(messageElements[2]).toHaveTextContent('How are you?');
    
    // Check sender attributes
    expect(messageElements[0]).toHaveAttribute('data-sender', 'user');
    expect(messageElements[1]).toHaveAttribute('data-sender', 'bot');
    expect(messageElements[2]).toHaveAttribute('data-sender', 'user');
  });

  test('passes correct message props to ChatMessage components', () => {
    render(<ChatHistory messages={mockMessages} />);
    
    const messageElements = screen.getAllByTestId('chat-message');
    
    expect(messageElements[0]).toHaveAttribute('data-message-id', '1');
    expect(messageElements[1]).toHaveAttribute('data-message-id', '2');
    expect(messageElements[2]).toHaveAttribute('data-message-id', '3');
  });

  // Testing the auto-scroll functionality would require more complex setup with jest-dom
  // and testing the scrollIntoView behavior, which is beyond the scope of this basic test
});