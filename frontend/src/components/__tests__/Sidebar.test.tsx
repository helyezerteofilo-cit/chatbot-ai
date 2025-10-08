import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Sidebar from '../Sidebar';
import { Chat } from '../../types';

// Mock the Logo component to simplify testing
jest.mock('../Logo', () => {
  return {
    __esModule: true,
    default: ({ size }: { size?: string }) => (
      <div data-testid="mock-logo" data-size={size}>
        Logo Component
      </div>
    ),
  };
});

describe('Sidebar Component', () => {
  const mockChats: Chat[] = [
    {
      id: '1',
      title: 'Chat 1',
      messages: [],
      createdAt: new Date('2023-05-15T10:00:00'),
    },
    {
      id: '2',
      title: 'Chat 2',
      messages: [],
      createdAt: new Date('2023-05-16T11:00:00'),
    },
  ];

  const mockOnSelectChat = jest.fn();
  const mockOnNewChat = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders sidebar with logo and new chat button', () => {
    render(
      <Sidebar
        chats={[]}
        activeChat={null}
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    expect(screen.getByTestId('mock-logo')).toBeInTheDocument();
    expect(screen.getByTestId('mock-logo')).toHaveAttribute('data-size', 'large');
    expect(screen.getByText('+ New Chat')).toBeInTheDocument();
  });

  test('displays "No previous chats" when chat list is empty', () => {
    render(
      <Sidebar
        chats={[]}
        activeChat={null}
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    expect(screen.getByText('No previous chats')).toBeInTheDocument();
  });

  test('renders chat list when chats are provided', () => {
    render(
      <Sidebar
        chats={mockChats}
        activeChat={null}
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    expect(screen.getByText('Chat 1')).toBeInTheDocument();
    expect(screen.getByText('Chat 2')).toBeInTheDocument();
    expect(screen.queryByText('No previous chats')).not.toBeInTheDocument();
  });

  test('sorts chats by creation date (newest first)', () => {
    render(
      <Sidebar
        chats={mockChats}
        activeChat={null}
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    const chatItems = screen.getAllByText(/Chat \d/);
    expect(chatItems[0].textContent).toBe('Chat 2'); // Newer chat should be first
    expect(chatItems[1].textContent).toBe('Chat 1');
  });

  test('applies active class to the selected chat', () => {
    render(
      <Sidebar
        chats={mockChats}
        activeChat="1"
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    const chatItems = screen.getAllByText(/Chat \d/).map(item => item.parentElement);
    expect(chatItems[1]).toHaveClass('active'); // Chat 1 should be active
    expect(chatItems[0]).not.toHaveClass('active'); // Chat 2 should not be active
  });

  test('calls onSelectChat when a chat is clicked', () => {
    render(
      <Sidebar
        chats={mockChats}
        activeChat={null}
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    fireEvent.click(screen.getByText('Chat 1'));
    expect(mockOnSelectChat).toHaveBeenCalledWith('1');
  });

  test('calls onNewChat when new chat button is clicked', () => {
    render(
      <Sidebar
        chats={[]}
        activeChat={null}
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    fireEvent.click(screen.getByText('+ New Chat'));
    expect(mockOnNewChat).toHaveBeenCalled();
  });

  test('displays formatted dates for chats', () => {
    render(
      <Sidebar
        chats={mockChats}
        activeChat={null}
        onSelectChat={mockOnSelectChat}
        onNewChat={mockOnNewChat}
      />
    );

    // The exact format will depend on the locale of the test environment
    // We're just checking that the date elements exist
    const dateElements = screen.getAllByText(/\d{1,2}\/\d{1,2}\/\d{4}/);
    expect(dateElements.length).toBe(2);
  });
});