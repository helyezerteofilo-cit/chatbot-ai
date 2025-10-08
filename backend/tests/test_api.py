import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

class TestAPIEndpoints:
    
    @patch('src.api.endpoints.chatbot_service')
    def test_chat_success(self, mock_chatbot_service, test_client):
        """Tests the chat endpoint with successful response"""
        # Arrange
        mock_chatbot_service.process_message = AsyncMock(return_value={
            "status": "success",
            "response": "Artificial Intelligence is a field of computer science...",
            "context": {
                "num_docs_retrieved": 2,
                "sources": [{"source": "sample.txt", "page": None}]
            }
        })
        
        # Act
        response = test_client.post(
            "/api/chat",
            json={"message": "What is Artificial Intelligence?"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Artificial Intelligence" in data["response"]
        assert data["context"]["num_docs_retrieved"] == 2
        mock_chatbot_service.process_message.assert_called_once_with("What is Artificial Intelligence?")
    
    @patch('src.api.endpoints.chatbot_service')
    def test_chat_error(self, mock_chatbot_service, test_client):
        """Tests the chat endpoint with error response"""
        # Arrange
        mock_chatbot_service.process_message = AsyncMock(return_value={
            "status": "error",
            "message": "Error generating response: API error"
        })
        
        # Act
        response = test_client.post(
            "/api/chat",
            json={"message": "What is Artificial Intelligence?"}
        )
        
        # Assert
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "API error" in data["detail"]
        mock_chatbot_service.process_message.assert_called_once_with("What is Artificial Intelligence?")
    
    def test_chat_empty_message(self, test_client):
        """Tests the chat endpoint with empty message"""
        # Act
        response = test_client.post(
            "/api/chat",
            json={"message": ""}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Message cannot be empty" in data["detail"]
    
    def test_chat_invalid_json(self, test_client):
        """Tests the chat endpoint with invalid JSON"""
        # Act
        response = test_client.post(
            "/api/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_chat_missing_message(self, test_client):
        """Tests the chat endpoint with missing message field"""
        # Act
        response = test_client.post(
            "/api/chat",
            json={}
        )
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity
    
    @patch('src.api.endpoints.document_service')
    def test_upload_document_success(self, mock_document_service, test_client):
        """Tests the document upload endpoint with successful response"""
        # Arrange
        mock_document_service.save_uploaded_document.return_value = {
            "status": "success",
            "message": "Document uploaded and processed successfully",
            "document_id": "test-uuid",
            "document_name": "test.pdf"
        }
        
        # Act
        with open("tests/test_api.py", "rb") as f:
            file_content = f.read()
        
        response = test_client.post(
            "/api/upload",
            files={"file": ("test.pdf", file_content, "application/pdf")}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["document_id"] == "test-uuid"
        assert data["document_name"] == "test.pdf"
        mock_document_service.save_uploaded_document.assert_called_once()
    
    @patch('src.api.endpoints.document_service')
    def test_upload_document_error(self, mock_document_service, test_client):
        """Tests the document upload endpoint with error response"""
        # Arrange
        mock_document_service.save_uploaded_document.return_value = {
            "status": "error",
            "message": "Error processing document"
        }
        
        # Act
        with open("tests/test_api.py", "rb") as f:
            file_content = f.read()
        
        response = test_client.post(
            "/api/upload",
            files={"file": ("test.pdf", file_content, "application/pdf")}
        )
        
        # Assert
        assert response.status_code == 500
        data = response.json()
        assert data["status"] == "error"
        assert "Error processing document" in data["message"]
        mock_document_service.save_uploaded_document.assert_called_once()
    
    def test_upload_document_unsupported_type(self, test_client):
        """Tests the document upload endpoint with unsupported file type"""
        # Act
        with open("tests/test_api.py", "rb") as f:
            file_content = f.read()
        
        response = test_client.post(
            "/api/upload",
            files={"file": ("test.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        
        # Assert
        assert response.status_code == 415
        data = response.json()
        assert data["status"] == "error"
        assert "Unsupported file type" in data["message"]