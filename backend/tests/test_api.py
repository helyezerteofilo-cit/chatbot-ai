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