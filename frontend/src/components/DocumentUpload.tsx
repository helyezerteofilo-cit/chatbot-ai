import React, { useState, useRef } from 'react';
import { uploadDocument } from '../services/api';
import '../styles/DocumentUpload.css';

interface DocumentUploadProps {
  onUploadSuccess: (documentName: string, documentId: string) => void;
  onUploadError: (errorMessage: string) => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ 
  onUploadSuccess, 
  onUploadError 
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      handleFileSelection(file);
    }
  };

  const handleFileSelection = (file: File) => {
    // Check file type
    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    if (fileExtension !== 'txt' && fileExtension !== 'pdf') {
      onUploadError('Only .txt and .pdf files are supported');
      return;
    }

    // Check file size (10MB max)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
      onUploadError('File size exceeds 10MB limit');
      return;
    }

    setSelectedFile(file);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const handleBrowseClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    
    try {
      // Use the uploadDocument function from api.ts
      const response = await uploadDocument(selectedFile);

      if (response.status === 'success' && response.document_id && response.document_name) {
        onUploadSuccess(response.document_name, response.document_id);
        setSelectedFile(null);
      } else {
        onUploadError(response.message || 'Upload failed');
      }
    } catch (error) {
      onUploadError('Error uploading document');
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleCancel = () => {
    setSelectedFile(null);
  };

  return (
    <div className="document-upload">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileInputChange}
        accept=".txt,.pdf"
        style={{ display: 'none' }}
      />

      {!selectedFile ? (
        <div
          className={`upload-area ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleBrowseClick}
        >
          <div className="upload-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <path fill="none" d="M0 0h24v24H0z"/>
              <path d="M12 12.586l4.243 4.242-1.415 1.415L13 16.415V22h-2v-5.587l-1.828 1.83-1.415-1.415L12 12.586zM12 2a7.001 7.001 0 0 1 6.954 6.194 5.5 5.5 0 0 1-.953 10.784v-2.014a3.5 3.5 0 1 0-1.112-6.91 5 5 0 1 0-9.777 0 3.5 3.5 0 0 0-1.292 6.88l.19.03v2.014a5.5 5.5 0 0 1-.954-10.784A7 7 0 0 1 12 2z" fill="currentColor"/>
            </svg>
          </div>
          <p>Drag and drop a document here, or click to browse</p>
          <p className="upload-hint">Supports .txt and .pdf files (max 10MB)</p>
        </div>
      ) : (
        <div className="selected-file">
          <div className="file-info">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <path fill="none" d="M0 0h24v24H0z"/>
              <path d="M3 8l6.003-6h10.995C20.55 2 21 2.455 21 2.992v18.016a.993.993 0 0 1-.993.992H3.993A1 1 0 0 1 3 20.993V8zm7-4.5L4.5 9H10V3.5z" fill="currentColor"/>
            </svg>
            <span className="file-name">{selectedFile.name}</span>
          </div>
          <div className="file-actions">
            <button 
              className="upload-button" 
              onClick={handleUpload}
              disabled={isUploading}
            >
              {isUploading ? 'Uploading...' : 'Upload'}
            </button>
            <button 
              className="cancel-button" 
              onClick={handleCancel}
              disabled={isUploading}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;