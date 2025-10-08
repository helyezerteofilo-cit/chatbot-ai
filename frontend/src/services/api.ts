import { MessageRequest, MessageResponse } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const sendMessage = async (message: string): Promise<MessageResponse> => {
  try {
    const request: MessageRequest = { message };
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to send message');
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message:', error);
    return {
      response: 'Sorry, there was an error processing your request.',
      status: 'error',
    };
  }
};
