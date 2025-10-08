# CI&T Flow RAG Chatbot - Backend

A chatbot that uses Retrieval-Augmented Generation (RAG) with CI&T Flow API to provide context-aware responses based on your documents.

## Features

- Integration with CI&T Flow API for LLM capabilities
- Document loading and processing (text and PDF files)
- Document upload functionality for user-provided context
- RAG implementation for context-aware responses
- FastAPI backend with API endpoints

## Project Structure

```
backend/
├── docs/                  # Folder for storing pre-loaded documents for RAG
├── uploads/               # Folder for storing user-uploaded documents
├── src/
│   ├── api/               # API endpoints
│   ├── config/            # Configuration settings
│   ├── models/            # Pydantic models
│   ├── services/          # Business logic services
│   └── main.py            # Main application entry point
├── .env                   # Environment variables (not in git)
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Setup

1. Clone the repository
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
5. Create a `.env` file based on `.env.example` and fill in your CI&T Flow API token:
   ```bash
   cp .env.example .env
   # Edit .env with your API token
   ```
6. Add your documents to the `docs` folder (supported formats: .txt, .pdf)

## Running the Application

Start the FastAPI server:

```bash
cd backend
python -m src.main
```

The API will be available at http://localhost:8000

## API Endpoints

- `POST /api/chat` - Chat endpoint for sending messages and receiving responses
- `POST /api/upload` - Upload endpoint for adding documents to the RAG system

## Example Usage

```bash
# Send a message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What information do you have about project X?"}'

# Upload a document
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/your/document.pdf"
```

## Document Upload

The system supports uploading the following document types:
- Text files (.txt)
- PDF files (.pdf)

Uploaded documents are automatically processed and added to the RAG system, making their content available for future queries. The maximum upload size is 10MB by default, which can be configured in the `.env` file.