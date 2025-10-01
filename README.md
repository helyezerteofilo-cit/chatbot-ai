# CI&T Flow RAG Chatbot

A chatbot that uses Retrieval-Augmented Generation (RAG) with CI&T Flow API to provide context-aware responses based on your documents.

## Project Structure

This project is organized into the following directories:

```
.
└── backend/              # Backend implementation
    ├── docs/             # Documents for RAG
    ├── src/              # Source code
    └── ...               # Configuration files
```

## Backend

The backend is built with FastAPI and implements:
- CI&T Flow API integration
- Document loading and processing (RAG)
- Chat API endpoints

For more details, see the [backend README](backend/README.md).

## Getting Started

To get started with the project:

1. Set up the backend:
   ```bash
   cd backend
   # Follow the instructions in the backend README
   ```

## User Stories Implemented

### User Story 1: Backend - CI&T Flow API Integration Setup
- Backend set up using FastAPI
- Configuration file for API token and RAG documents folder
- Connection to CI&T Flow APIs
- Health check API endpoint

### User Story 2: Backend - RAG Document Loading and Processing
- Document loading from specified folder
- Support for text and PDF files
- Document parsing and chunking
- Embedding process configuration

### User Story 3: Backend - Message Handling and RAG + CI&T Flow Integration
- API endpoint for receiving messages
- RAG implementation for retrieving relevant document chunks
- Integration with CI&T Flow APIs for LLM responses
- Response handling and delivery