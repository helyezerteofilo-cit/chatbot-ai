import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@pytest.fixture
def mock_document_service():
    with patch("src.api.endpoints.document_service") as mock_service:
        yield mock_service

def test_upload_document_success(mock_document_service):
    # Mock the save_uploaded_document method
    mock_document_service.save_uploaded_document.return_value = {
        "status": "success",
        "message": "Document uploaded and processed successfully",
        "document_id": "test-uuid",
        "document_name": "test.pdf"
    }
    
    # Create a test file
    test_file_content = b"This is a test PDF file content"
    
    # Make the request
    response = client.post(
        "/api/upload",
        files={"file": ("test.pdf", test_file_content, "application/pdf")}
    )
    
    # Check the response
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Document uploaded and processed successfully",
        "document_id": "test-uuid",
        "document_name": "test.pdf"
    }
    
    # Verify the service was called correctly
    mock_document_service.save_uploaded_document.assert_called_once()
    args, kwargs = mock_document_service.save_uploaded_document.call_args
    assert args[0] == test_file_content
    assert args[1] == "test.pdf"

def test_upload_document_unsupported_type(mock_document_service):
    # Create a test file with unsupported extension
    test_file_content = b"This is a test file content"
    
    # Make the request
    response = client.post(
        "/api/upload",
        files={"file": ("test.docx", test_file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
    
    # Check the response
    assert response.status_code == 415
    assert response.json()["status"] == "error"
    assert "Unsupported file type" in response.json()["message"]
    
    # Verify the service was not called
    mock_document_service.save_uploaded_document.assert_not_called()

def test_upload_document_too_large(mock_document_service):
    # Create a test file that's larger than the limit
    # We'll patch the MAX_UPLOAD_SIZE to a small value for testing
    with patch("src.config.settings.settings.MAX_UPLOAD_SIZE", 10):
        test_file_content = b"This is a test file content that exceeds the size limit"
        
        # Make the request
        response = client.post(
            "/api/upload",
            files={"file": ("test.pdf", test_file_content, "application/pdf")}
        )
        
        # Check the response
        assert response.status_code == 413
        assert response.json()["status"] == "error"
        assert "File too large" in response.json()["message"]
        
        # Verify the service was not called
        mock_document_service.save_uploaded_document.assert_not_called()

def test_upload_document_error(mock_document_service):
    # Mock the save_uploaded_document method to return an error
    mock_document_service.save_uploaded_document.return_value = {
        "status": "error",
        "message": "Error processing document"
    }
    
    # Create a test file
    test_file_content = b"This is a test PDF file content"
    
    # Make the request
    response = client.post(
        "/api/upload",
        files={"file": ("test.pdf", test_file_content, "application/pdf")}
    )
    
    # Check the response
    assert response.status_code == 500
    assert response.json() == {
        "status": "error",
        "message": "Error processing document"
    }
    
    # Verify the service was called
    mock_document_service.save_uploaded_document.assert_called_once()