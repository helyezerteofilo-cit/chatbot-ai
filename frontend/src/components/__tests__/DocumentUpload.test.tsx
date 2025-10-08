import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import DocumentUpload from '../DocumentUpload';
import * as apiService from '../../services/api';

// Mock the api service
jest.mock('../../services/api', () => ({
  uploadDocument: jest.fn()
}));

describe('DocumentUpload Component', () => {
  const mockOnUploadSuccess = jest.fn();
  const mockOnUploadError = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  test('renders upload area initially', () => {
    render(
      <DocumentUpload 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    expect(screen.getByText(/Drag and drop a document here/i)).toBeInTheDocument();
    expect(screen.getByText(/Supports .txt and .pdf files/i)).toBeInTheDocument();
  });
  
  test('shows selected file when file is chosen', () => {
    render(
      <DocumentUpload 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const fileInput = document.querySelector('input[type=file]') as HTMLInputElement;
    
    Object.defineProperty(fileInput, 'files', {
      value: [file]
    });
    
    fireEvent.change(fileInput);
    
    expect(screen.getByText('test.txt')).toBeInTheDocument();
    expect(screen.getByText('Upload')).toBeInTheDocument();
    expect(screen.getByText('Cancel')).toBeInTheDocument();
  });
  
  test('calls onUploadError when file type is not supported', () => {
    render(
      <DocumentUpload 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    const fileInput = document.querySelector('input[type=file]') as HTMLInputElement;
    
    Object.defineProperty(fileInput, 'files', {
      value: [file]
    });
    
    fireEvent.change(fileInput);
    
    expect(mockOnUploadError).toHaveBeenCalledWith('Only .txt and .pdf files are supported');
  });
  
  test('uploads file when upload button is clicked', async () => {
    // Mock the uploadDocument function
    (apiService.uploadDocument as jest.Mock).mockResolvedValueOnce({
      status: 'success',
      message: 'Document uploaded successfully',
      document_id: '123',
      document_name: 'test.txt'
    });
    
    render(
      <DocumentUpload 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const fileInput = document.querySelector('input[type=file]') as HTMLInputElement;
    
    Object.defineProperty(fileInput, 'files', {
      value: [file]
    });
    
    fireEvent.change(fileInput);
    
    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);
    
    await waitFor(() => {
      expect(apiService.uploadDocument).toHaveBeenCalledWith(file);
      expect(mockOnUploadSuccess).toHaveBeenCalledWith('test.txt', '123');
    });
  });
  
  test('handles upload error', async () => {
    // Mock the uploadDocument function with an error
    (apiService.uploadDocument as jest.Mock).mockResolvedValueOnce({
      status: 'error',
      message: 'Upload failed'
    });
    
    render(
      <DocumentUpload 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const fileInput = document.querySelector('input[type=file]') as HTMLInputElement;
    
    Object.defineProperty(fileInput, 'files', {
      value: [file]
    });
    
    fireEvent.change(fileInput);
    
    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);
    
    await waitFor(() => {
      expect(apiService.uploadDocument).toHaveBeenCalledWith(file);
      expect(mockOnUploadError).toHaveBeenCalledWith('Upload failed');
    });
  });
  
  test('clears selected file when cancel is clicked', () => {
    render(
      <DocumentUpload 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const fileInput = document.querySelector('input[type=file]') as HTMLInputElement;
    
    Object.defineProperty(fileInput, 'files', {
      value: [file]
    });
    
    fireEvent.change(fileInput);
    
    expect(screen.getByText('test.txt')).toBeInTheDocument();
    
    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);
    
    expect(screen.queryByText('test.txt')).not.toBeInTheDocument();
    expect(screen.getByText(/Drag and drop a document here/i)).toBeInTheDocument();
  });
});
