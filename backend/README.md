# RAG Chatbot Backend

This is the backend service for the RAG-powered chatbot application. It provides document processing, vector storage, and AI integration capabilities.

## Overview

The backend is built with FastAPI and provides a RESTful API for:
- Processing and storing documents
- Retrieving relevant information from documents
- Generating AI responses using RAG (Retrieval-Augmented Generation)

## Project Structure

```
backend/
├── src/
│   ├── api/
│   │   └── endpoints.py       # API endpoints for chat and document upload
│   ├── config/
│   │   └── settings.py        # Application configuration
│   ├── services/
│   │   ├── chatbot_service.py # Coordinates RAG and LLM services
│   │   ├── flow_api.py        # Integration with CI&T Flow API
│   │   └── document/          # Document processing module
│   │       ├── __init__.py    # Package definition and exports
│   │       ├── document_service.py    # Main document service interface
│   │       ├── document_loader.py     # Document loading utilities
│   │       ├── document_processor.py  # Text processing and chunking
│   │       ├── vector_store_manager.py # Vector database management
│   │       └── upload_handler.py      # Document upload processing
│   ├── utils/
│   │   └── chunks_sanitizer.py # Text cleaning utilities
│   └── main.py                # Application entry point
├── docs/                      # Documentation files
├── uploads/                   # Uploaded documents storage
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Development dependencies
└── .env                       # Environment variables (not in git)
```

## Setup and Installation

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and fill in your CI&T Flow API token:
   ```
   FLOW_API_BASE_URL=your_api_base_url
   FLOW_MODEL=your_model_name
   FLOW_AGENT=your_agent_id
   FLOW_TENANT=your_tenant_id
   ```

### Running the Server

```bash
uvicorn src.main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### Chat Endpoint

```
POST /api/chat
```

Request body:
```json
{
  "message": "Your question here"
}
```

Response:
```json
{
  "response": "AI-generated response",
  "status": "success",
  "context": {
    "num_docs_retrieved": 3,
    "sources": [
      {
        "source": "document1.pdf",
        "page": 5
      },
      {
        "source": "document2.txt",
        "page": null
      }
    ]
  }
}
```

### Document Upload Endpoint

```
POST /api/upload
```

Form data:
- `file`: The document file (PDF or TXT)

Response:
```json
{
  "status": "success",
  "message": "Document uploaded successfully",
  "document_id": "unique-id",
  "document_name": "document.pdf"
}
```

## Key Components

### Document Service

The `DocumentService` class is the main interface for document operations:

- Loading documents from configured folders
- Processing and chunking documents
- Managing the vector store
- Handling document uploads

### Vector Store Manager

The `VectorStoreManager` handles:

- Creating and maintaining the vector database
- Adding new documents to the store
- Querying the store for relevant documents
- Scoring and filtering results by relevance

### Document Processor

The `DocumentProcessor` handles:

- Splitting documents into manageable chunks
- Processing text for better retrieval
- Sanitizing text content

### Flow API Service

The `FlowAPIService` handles:

- Authentication with the CI&T Flow API
- Generating responses using the LLM
- Providing context from retrieved documents

## Development

### Running Tests

```bash
pytest
```

### Adding New Document Types

To add support for new document types:

1. Update the file extension check in `endpoints.py`
2. Add appropriate document loaders in `document_loader.py`

## Troubleshooting

### Common Issues

- **ModuleNotFoundError: No module named 'langchain_chroma'**
  
  Solution: Install the missing package:
  ```bash
  pip install langchain-chroma
  ```

- **Error uploading document**
  
  Check that the uploads directory exists and has write permissions.

## License

This project is licensed under the MIT License.