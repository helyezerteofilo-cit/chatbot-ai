import { MessageRequest, MessageResponse, DocumentUploadResponse } from '../types';

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

export const uploadDocument = async (file: File): Promise<DocumentUploadResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to upload document');
    }

    return await response.json();
  } catch (error) {
    console.error('Error uploading document:', error);
    return {
      status: 'error',
      message: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
};