# RAG-Powered Chatbot

A modern chatbot application leveraging Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses based on your documents.

## Features

- **Document Processing**: Upload and process various document formats (PDF, TXT)
- **Retrieval-Augmented Generation**: Enhance AI responses with relevant information from your documents
- **Vector Search**: Semantic search capabilities for finding the most relevant document chunks
- **Web Interface**: Clean, responsive UI for interacting with the chatbot
- **Document Management**: Upload, view, and manage your knowledge base

## Architecture

The application consists of two main components:

### Backend (FastAPI)

The backend is built with FastAPI and provides:

- REST API endpoints for chat and document management
- Document processing pipeline
- Vector store for semantic search
- Integration with LLM APIs

### Frontend

The frontend provides:

- Chat interface
- Document upload and management
- Response visualization

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- pip
- npm or yarn

### Installation

#### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example` and fill in your API credentials:
   ```
   FLOW_API_BASE_URL=your_api_base_url
   FLOW_MODEL=your_model_name
   FLOW_AGENT=your_agent_id
   FLOW_TENANT=your_tenant_id
   ```

6. Start the backend server:
   ```bash
   uvicorn src.main:app --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Usage

### Uploading Documents

1. Click on the "Upload" button in the sidebar
2. Select a PDF or TXT file (max size: 10MB)
3. Wait for the document to be processed
4. The document will appear in your document list

### Chatting with the AI

1. Type your question in the chat input
2. The AI will respond using information from your uploaded documents
3. Sources used to generate the response will be displayed below the answer

## Technical Details

### Document Processing Pipeline

The system processes documents through several stages:

1. **Loading**: Documents are loaded from files using appropriate loaders
2. **Chunking**: Documents are split into manageable chunks
3. **Cleaning**: Text is normalized and cleaned
4. **Embedding**: Text chunks are converted to vector embeddings
5. **Indexing**: Embeddings are stored in a vector database for retrieval

### RAG Implementation

The RAG system works as follows:

1. User query is received
2. Most relevant document chunks are retrieved from the vector store
3. Retrieved chunks are provided as context to the LLM
4. LLM generates a response based on the provided context
5. Response is returned to the user with source information

## Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── endpoints.py       # API endpoints
│   │   ├── config/
│   │   │   └── settings.py        # Application settings
│   │   ├── services/
│   │   │   ├── chatbot_service.py # Chatbot logic
│   │   │   ├── flow_api.py        # LLM API integration
│   │   │   └── document/          # Document processing
│   │   │       ├── __init__.py
│   │   │       ├── document_service.py
│   │   │       ├── document_loader.py
│   │   │       ├── document_processor.py
│   │   │       ├── vector_store_manager.py
│   │   │       └── upload_handler.py
│   │   ├── utils/
│   │   │   └── chunks_sanitizer.py # Text cleaning utilities
│   │   └── main.py                # Application entry point
│   ├── docs/                      # Documentation files
│   ├── uploads/                   # Uploaded documents
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment variables
└── frontend/
    ├── src/
    │   ├── components/            # React components
    │   ├── types.ts               # TypeScript type definitions
    │   └── ...
    ├── package.json               # Node.js dependencies
    └── ...
```