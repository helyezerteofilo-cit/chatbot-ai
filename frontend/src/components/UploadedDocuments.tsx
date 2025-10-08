import React from 'react';
import '../styles/UploadedDocuments.css';

export interface UploadedDocument {
  id: string;
  name: string;
}

interface UploadedDocumentsProps {
  documents: UploadedDocument[];
}

const UploadedDocuments: React.FC<UploadedDocumentsProps> = ({ documents }) => {
  if (documents.length === 0) {
    return null;
  }

  return (
    <div className="uploaded-documents">
      <h3>Uploaded Documents</h3>
      <ul className="document-list">
        {documents.map((doc) => (
          <li key={doc.id} className="document-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
              <path fill="none" d="M0 0h24v24H0z"/>
              <path d="M3 8l6.003-6h10.995C20.55 2 21 2.455 21 2.992v18.016a.993.993 0 0 1-.993.992H3.993A1 1 0 0 1 3 20.993V8zm7-4.5L4.5 9H10V3.5z" fill="currentColor"/>
            </svg>
            <span className="document-name">{doc.name}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UploadedDocuments;