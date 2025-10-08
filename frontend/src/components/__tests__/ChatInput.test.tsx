import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatInput from '../ChatInput';

describe('ChatInput Component', () => {
  const mockSendMessage = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders input field and send button', () => {
    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);
    
    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
  });

  test('updates input value when typing', () => {
    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);
    
    const input = screen.getByPlaceholderText('Type your message here...') as HTMLInputElement;
    fireEvent.change(input, { target: { value: 'Hello world' } });
    
    expect(input.value).toBe('Hello world');
  });

  test('calls onSendMessage when form is submitted', () => {
    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);
    
    const input = screen.getByPlaceholderText('Type your message here...') as HTMLInputElement;
    fireEvent.change(input, { target: { value: 'Hello world' } });
    
    const button = screen.getByRole('button', { name: 'Send' });
    fireEvent.click(button);
    
    expect(mockSendMessage).toHaveBeenCalledWith('Hello world');
    expect(input.value).toBe(''); // Input should be cleared after sending
  });

  test('prevents form submission when input is empty', () => {
    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);
    
    const button = screen.getByRole('button', { name: 'Send' });
    expect(button).toBeDisabled();
    
    fireEvent.click(button);
    expect(mockSendMessage).not.toHaveBeenCalled();
  });

  test('disables input and shows loading state when isLoading is true', () => {
    render(<ChatInput onSendMessage={mockSendMessage} isLoading={true} />);
    
    const input = screen.getByPlaceholderText('Type your message here...') as HTMLInputElement;
    expect(input).toBeDisabled();
    
    const button = screen.getByRole('button', { name: 'Sending...' });
    expect(button).toBeDisabled();
  });

  test('trims whitespace from message before sending', () => {
    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);
    
    const input = screen.getByPlaceholderText('Type your message here...') as HTMLInputElement;
    fireEvent.change(input, { target: { value: '  Hello world  ' } });
    
    const button = screen.getByRole('button', { name: 'Send' });
    fireEvent.click(button);
    
    expect(mockSendMessage).toHaveBeenCalledWith('  Hello world  ');
  });

  test('prevents submission when only whitespace is entered', () => {
    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);
    
    const input = screen.getByPlaceholderText('Type your message here...') as HTMLInputElement;
    fireEvent.change(input, { target: { value: '   ' } });
    
    const button = screen.getByRole('button', { name: 'Send' });
    expect(button).toBeDisabled();
  });
});