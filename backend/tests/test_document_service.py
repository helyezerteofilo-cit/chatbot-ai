import os
import pytest
from unittest.mock import patch, MagicMock
from src.services.document_service import DocumentService

class TestDocumentService:
    
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    def test_init(self, mock_settings, mock_embeddings):
        """Tests the initialization of DocumentService"""
        # Arrange
        mock_settings.RAG_DOCUMENTS_FOLDER = "docs"
        mock_settings.VECTOR_STORE_PATH = "vector_store"
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        # Act
        service = DocumentService()
        
        # Assert
        assert "docs" in service.documents_folder
        assert "vector_store" in service.vector_store_path
        assert service.embedding_model_name == "test-model"
        assert service.embeddings == mock_embeddings_instance
        mock_embeddings.assert_called_once_with(model_name="test-model")
    
    @patch('src.services.document_service.TextLoader')
    @patch('src.services.document_service.settings')
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('os.path.exists')
    @patch('os.walk')
    def test_load_documents(self, mock_walk, mock_exists, mock_embeddings, mock_settings, mock_text_loader):
        """Tests loading documents"""
        # Arrange
        mock_settings.RAG_DOCUMENTS_FOLDER = "docs"
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        mock_exists.return_value = True
        mock_walk.return_value = [("/fake/path", [], ["doc1.txt", "doc2.pdf"])]
        
        mock_text_loader_instance = MagicMock()
        mock_text_loader.return_value = mock_text_loader_instance
        mock_text_loader_instance.load.return_value = ["loaded text document"]
        
        mock_pdf_loader = MagicMock()
        with patch('src.services.document_service.PyPDFLoader', return_value=mock_pdf_loader) as mock_pdf_loader_class:
            mock_pdf_loader.load.return_value = ["loaded pdf document"]
            
            service = DocumentService()
            
            # Act
            documents = service.load_documents()
            
            # Assert
            assert len(documents) == 2
            mock_text_loader.assert_called_once()
            mock_pdf_loader_class.assert_called_once()
            mock_text_loader_instance.load.assert_called_once()
            mock_pdf_loader.load.assert_called_once()
    
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    def test_process_documents(self, mock_settings, mock_embeddings):
        """Tests document processing"""
        # Arrange
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        service = DocumentService()
        mock_documents = [MagicMock(), MagicMock()]
        service.text_splitter = MagicMock()
        service.text_splitter.split_documents.return_value = ["chunk1", "chunk2", "chunk3"]
        
        # Act
        result = service.process_documents(mock_documents)
        
        # Assert
        assert len(result) == 3
        service.text_splitter.split_documents.assert_called_once_with(mock_documents)
    
    @patch('src.services.document_service.Chroma')
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    @patch('os.path.exists')
    @patch('shutil.rmtree')
    @patch('os.makedirs')
    def test_create_vector_store(self, mock_makedirs, mock_rmtree, mock_exists, mock_settings, mock_embeddings, mock_chroma):
        """Tests creating vector store using Chroma"""
        # Arrange
        mock_settings.VECTOR_STORE_PATH = "vector_store"
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        mock_exists.return_value = True
        
        mock_vector_store = MagicMock()
        mock_chroma.from_documents.return_value = mock_vector_store
        
        service = DocumentService()
        
        # Act
        documents = [MagicMock(), MagicMock()]
        result = service.create_vector_store(documents)
        
        # Assert
        assert result == mock_vector_store
        mock_rmtree.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_chroma.from_documents.assert_called_once_with(
            documents=documents,
            embedding=service.embeddings,
            persist_directory=service.vector_store_path
        )
        mock_vector_store.persist.assert_called_once()
    
    @patch('src.services.document_service.Chroma')
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    @patch('os.path.exists')
    def test_load_vector_store(self, mock_exists, mock_settings, mock_embeddings, mock_chroma):
        """Tests loading the vector store"""
        # Arrange
        mock_settings.VECTOR_STORE_PATH = "vector_store"
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        mock_exists.return_value = True
        
        mock_vector_store = MagicMock()
        mock_chroma.return_value = mock_vector_store
        
        service = DocumentService()
        
        # Act
        result = service.load_vector_store()
        
        # Assert
        assert result == mock_vector_store
        mock_chroma.assert_called_once_with(
            persist_directory=service.vector_store_path,
            embedding_function=service.embeddings
        )
    
    @patch('src.services.document_service.Chroma')
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    @patch('os.path.exists')
    def test_query_vector_store(self, mock_exists, mock_settings, mock_embeddings, mock_chroma):
        """Tests querying the vector store"""
        # Arrange
        mock_settings.VECTOR_STORE_PATH = "vector_store"
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        mock_exists.return_value = True
        
        mock_vector_store = MagicMock()
        mock_chroma.return_value = mock_vector_store
        mock_vector_store.similarity_search.return_value = ["doc1", "doc2"]
        
        service = DocumentService()
        
        # Act
        result = service.query_vector_store("What is AI?", k=2)
        
        # Assert
        assert result == ["doc1", "doc2"]
        mock_vector_store.similarity_search.assert_called_once_with("What is AI?", k=2)
    
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    def test_setup_rag_system_success(self, mock_settings, mock_embeddings):
        """Tests successful RAG system setup"""
        # Arrange
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        service = DocumentService()
        service.load_documents = MagicMock(return_value=["doc1", "doc2"])
        service.process_documents = MagicMock(return_value=["chunk1", "chunk2", "chunk3"])
        service.create_vector_store = MagicMock()
        
        # Act
        result = service.setup_rag_system()
        
        # Assert
        assert result["status"] == "success"
        assert "Successfully processed 2 documents into 3 chunks" in result["message"]
        service.load_documents.assert_called_once()
        service.process_documents.assert_called_once_with(["doc1", "doc2"])
        service.create_vector_store.assert_called_once_with(["chunk1", "chunk2", "chunk3"])
    
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    def test_setup_rag_system_no_documents(self, mock_settings, mock_embeddings):
        """Tests RAG system setup with no documents"""
        # Arrange
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        service = DocumentService()
        service.load_documents = MagicMock(return_value=[])
        
        # Act
        result = service.setup_rag_system()
        
        # Assert
        assert result["status"] == "warning"
        assert "No documents found to process" in result["message"]
        service.load_documents.assert_called_once()
        
    @patch('src.services.document_service.HuggingFaceEmbeddings')
    @patch('src.services.document_service.settings')
    def test_setup_rag_system_error(self, mock_settings, mock_embeddings):
        """Tests RAG system setup with error"""
        # Arrange
        mock_settings.EMBEDDING_MODEL = "test-model"
        
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        service = DocumentService()
        service.load_documents = MagicMock(side_effect=Exception("Test error"))
        
        # Act
        result = service.setup_rag_system()
        
        # Assert
        assert result["status"] == "error"
        assert "Error setting up RAG system: Test error" in result["message"]
        service.load_documents.assert_called_once()