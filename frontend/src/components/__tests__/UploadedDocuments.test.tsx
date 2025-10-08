import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import UploadedDocuments from '../UploadedDocuments';

describe('UploadedDocuments Component', () => {
  test('renders nothing when no documents are provided', () => {
    const { container } = render(<UploadedDocuments documents={[]} />);
    expect(container.firstChild).toBeNull();
  });

  test('renders documents when provided', () => {
    const documents = [
      { id: '1', name: 'document1.txt' },
      { id: '2', name: 'document2.pdf' }
    ];
    
    render(<UploadedDocuments documents={documents} />);
    
    expect(screen.getByText('Uploaded Documents')).toBeInTheDocument();
    expect(screen.getByText('document1.txt')).toBeInTheDocument();
    expect(screen.getByText('document2.pdf')).toBeInTheDocument();
  });

  test('renders correct number of document items', () => {
    const documents = [
      { id: '1', name: 'document1.txt' },
      { id: '2', name: 'document2.pdf' },
      { id: '3', name: 'document3.txt' }
    ];
    
    render(<UploadedDocuments documents={documents} />);
    
    const documentItems = screen.getAllByRole('listitem');
    expect(documentItems).toHaveLength(3);
  });
});