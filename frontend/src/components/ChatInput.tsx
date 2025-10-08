import React, { useState, useRef } from 'react';
import { uploadDocument } from '../services/api';
import '../styles/ChatInput.css';

interface ChatInputProps {
  onSendMessage: (message: string, attachments?: { id: string; name: string }[]) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  isLoading
}) => {
  const [message, setMessage] = useState('');
  const [attachedFiles, setAttachedFiles] = useState<{ id: string; name: string; file: File }[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if ((!message.trim() && attachedFiles.length === 0) || isLoading || isUploading) {
      return;
    }

    let uploadedAttachments: { id: string; name: string }[] = [];

    // First upload any attached files
    if (attachedFiles.length > 0) {
      setIsUploading(true);
      try {
        for (const attachedFile of attachedFiles) {
          const response = await uploadDocument(attachedFile.file);
          if (response.status === 'success' && response.document_id) {
            uploadedAttachments.push({
              id: response.document_id,
              name: response.document_name || attachedFile.name
            });
          }
        }
      } catch (error) {
        console.error('Error uploading files:', error);
        // Continue with message even if upload fails
      } finally {
        setIsUploading(false);
      }
    }

    // Then send the message with attachments
    onSendMessage(message.trim() || 'Document uploaded', uploadedAttachments);
    setMessage('');
    setAttachedFiles([]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const newFiles = Array.from(files).map(file => ({
        id: Math.random().toString(36).substr(2, 9),
        name: file.name,
        file
      }));
      setAttachedFiles(prev => [...prev, ...newFiles]);
    }
    // Reset the input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeAttachment = (id: string) => {
    setAttachedFiles(prev => prev.filter(file => file.id !== id));
  };

  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  // Function to truncate long filenames for attachment display
  const truncateFilename = (filename: string, maxLength: number = 25) => {
    if (filename.length <= maxLength) return filename;
    
    const extension = filename.split('.').pop();
    const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
    const truncatedName = nameWithoutExt.substring(0, maxLength - extension!.length - 4) + '...';
    
    return `${truncatedName}.${extension}`;
  };

  return (
    <div className="chat-input-wrapper">
      {/* Show attached files */}
      {attachedFiles.length > 0 && (
        <div className="attached-files">
          {attachedFiles.map(file => (
            <div key={file.id} className="attached-file" title={file.name}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
              <span className="file-name">{truncateFilename(file.name)}</span>
              <button 
                type="button" 
                className="remove-file"
                onClick={() => removeAttachment(file.id)}
                title="Remove file"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}
      
      <form className="chat-input-container" onSubmit={handleSubmit}>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt"
          multiple
          style={{ display: 'none' }}
          onChange={handleFileSelect}
        />
        
        <button 
          type="button" 
          className="attachment-button"
          onClick={triggerFileSelect}
          title="Attach document"
          disabled={isLoading || isUploading}
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="none">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66L9.64 16.2a2 2 0 0 1-2.83-2.83l8.49-8.49" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"/>
          </svg>
        </button>
        
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder={attachedFiles.length > 0 ? "Add a message (optional)..." : "Type your message here..."}
          disabled={isLoading || isUploading}
          className="chat-input"
        />
        
        <button 
          type="submit" 
          disabled={(!message.trim() && attachedFiles.length === 0) || isLoading || isUploading}
          className="send-button"
        >
          {isUploading ? 'Uploading...' : isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInput;
