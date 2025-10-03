import os
import sys
import pytest
import tempfile
import shutil
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.main import app
from src.services.document_service import DocumentService
from src.services.flow_api import FlowAPIService

@pytest.fixture
def test_client():
    """
    Creates a test client for the FastAPI application
    """
    return TestClient(app)

@pytest.fixture
def mock_flow_api():
    """
    Creates a mock of the FlowAPIService
    """
    with patch('src.services.flow_api.FlowAPIService') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_document_service():
    """
    Creates a mock of the DocumentService
    """
    with patch('src.services.document_service.DocumentService') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def temp_docs_dir():
    """
    Creates a temporary directory for test documents
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def temp_vector_store():
    """
    Creates a temporary directory for the vector store
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_document(temp_docs_dir):
    """
    Creates a sample document for testing
    """
    content = """
    Title: Introduction to Artificial Intelligence
    1. What is Artificial Intelligence (AI)?
    Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence.
    """
    file_path = os.path.join(temp_docs_dir, "sample.txt")
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

@pytest.fixture
def full_sample_document(temp_docs_dir):
    """
    Creates a complete sample document for testing
    """
    content = """
    Title: Introduction to Artificial Intelligence
    1. What is Artificial Intelligence (AI)?
    Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence. This includes abilities such as learning, reasoning, perception, and language understanding. There are two main categories of AI:

    Weak AI: Systems designed to perform specific tasks, such as virtual assistants and recommendation systems.
    Strong AI: Theoretically, systems that possess consciousness and understanding comparable to humans.
    
    2. History of Artificial Intelligence
    AI has its roots in various disciplines, such as mathematics, psychology, neuroscience, and philosophy. The concept of thinking machines dates back to philosophical articles in the 20th century, but the term "Artificial Intelligence" was coined in 1956 during the Dartmouth Conference. Since then, AI has evolved significantly through various revolutions, including progress in machine learning algorithms and neural networks.
    """
    file_path = os.path.join(temp_docs_dir, "full_sample.txt")
    with open(file_path, "w") as f:
        f.write(content)
    return file_path