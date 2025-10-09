# RAG Chatbot Frontend

This is the frontend application for the RAG-powered chatbot. It provides a user interface for interacting with the chatbot, uploading documents, and viewing responses with source attribution.

## Features

- Interactive chat interface with message history
- Document upload functionality supporting PDF and TXT files
- Document management and organization
- Response visualization with source attribution from retrieved documents
- Responsive design for desktop and mobile devices

## Tech Stack

- React with TypeScript
- Modern UI components with styled-components
- State management with React Context API
- API integration with Fetch API
- File handling with react-dropzone

## Project Structure

```
frontend/
├── public/
│   └── assets/
├── src/
│   ├── components/
│   │   ├── Chat/
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ChatContainer.tsx
│   │   ├── Documents/
│   │   │   ├── DocumentUpload.tsx
│   │   │   └── DocumentList.tsx
│   │   └── Layout/
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── MainLayout.tsx
│   ├── contexts/
│   │   ├── ChatContext.tsx
│   │   └── DocumentContext.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── chatService.ts
│   │   └── documentService.ts
│   ├── types.ts
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── validators.ts
│   └── App.tsx
├── package.json
├── tsconfig.json
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Create a `.env` file with your environment variables:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Integration

The frontend communicates with the backend through the following endpoints:

### Chat API

```typescript
// Send a message to the chatbot
const sendMessage = async (message: string): Promise<MessageResponse> => {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to send message');
  }
  
  return response.json();
};
```

### Document Upload API

```typescript
// Upload a document
const uploadDocument = async (file: File): Promise<DocumentUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_URL}/api/upload`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Failed to upload document');
  }
  
  return response.json();
};
```

## Key Components

### ChatContainer

The main chat interface that:
- Displays the conversation history
- Handles user input submission
- Shows typing indicators
- Renders source attribution for AI responses

### ChatMessage

Renders individual chat messages with:
- Different styling for user and AI messages
- Source attribution links
- Timestamp display
- Markdown rendering for formatted responses

### DocumentUpload

Provides document upload functionality with:
- Drag-and-drop interface
- File type validation
- Size limit enforcement
- Upload progress indicator
- Error handling

### DocumentList

Displays uploaded documents with:
- Document name and type
- Upload date
- File size
- Delete functionality

## Type Definitions

The application uses TypeScript interfaces to ensure type safety:

```typescript
export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  attachments?: MessageAttachment[];
}

export interface MessageAttachment {
  id: string;
  name: string;
  type: 'document';
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  documents?: UploadedDocument[];
}

export interface MessageRequest {
  message: string;
}

export interface MessageResponse {
  response: string;
  status: string;
  context?: Record<string, any>;
}

export interface UploadedDocument {
  id: string;
  name: string;
}

export interface DocumentUploadResponse {
  status: string;
  message: string;
  document_id?: string;
  document_name?: string;
}
```