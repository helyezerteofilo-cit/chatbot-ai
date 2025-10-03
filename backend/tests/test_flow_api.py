import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import pytest_asyncio
from src.services.flow_api import FlowAPIService

class TestFlowAPIService:
    
    @patch('src.services.flow_api.TokenManager')
    def test_init(self, mock_token_manager):
        """Tests the initialization of FlowAPIService"""
        # Arrange
        mock_token_manager_instance = MagicMock()
        mock_token_manager.return_value = mock_token_manager_instance
        
        # Act
        service = FlowAPIService()
        
        # Assert
        assert hasattr(service, 'token_manager')
        assert service.chat_model is None
        mock_token_manager.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.services.flow_api.TokenManager')
    @patch('src.services.flow_api.ChatOpenAI')
    async def test_get_chat_model(self, mock_chat_openai, mock_token_manager):
        """Tests getting the chat model"""
        # Arrange
        mock_token_manager_instance = AsyncMock()
        mock_token_manager_instance.get_valid_token.return_value = "test_token"
        mock_token_manager.return_value = mock_token_manager_instance
        
        mock_chat_model = MagicMock()
        mock_chat_openai.return_value = mock_chat_model
        
        service = FlowAPIService()
        
        # Act
        result = await service._get_chat_model()
        
        # Assert
        assert result == mock_chat_model
        mock_token_manager_instance.get_valid_token.assert_called_once()
        mock_chat_openai.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.services.flow_api.TokenManager')
    @patch('src.services.flow_api.ChatOpenAI')
    @patch('src.services.flow_api.SystemMessage')
    @patch('src.services.flow_api.HumanMessage')
    async def test_generate_response_without_context(self, mock_human_message, mock_system_message, mock_chat_openai, mock_token_manager):
        """Tests generating a response without context"""
        # Arrange
        mock_token_manager_instance = AsyncMock()
        mock_token_manager_instance.get_valid_token.return_value = "test_token"
        mock_token_manager.return_value = mock_token_manager_instance
        
        mock_chat_model = MagicMock()
        mock_chat_openai.return_value = mock_chat_model
        
        mock_system_msg = MagicMock()
        mock_system_message.return_value = mock_system_msg
        
        mock_human_msg = MagicMock()
        mock_human_message.return_value = mock_human_msg
        
        mock_response = MagicMock()
        mock_response.content = "This is a test response"
        mock_chat_model.invoke.return_value = mock_response
        
        service = FlowAPIService()
        
        # Act
        result = await service.generate_response("What is AI?")
        
        # Assert
        assert result["status"] == "success"
        assert result["response"] == "This is a test response"
        mock_system_message.assert_called_once_with(content="You are a helpful assistant.")
        mock_human_message.assert_called_once_with(content="What is AI?")
        mock_chat_model.invoke.assert_called_once_with([mock_system_msg, mock_human_msg])
    
    @pytest.mark.asyncio
    @patch('src.services.flow_api.TokenManager')
    @patch('src.services.flow_api.ChatOpenAI')
    @patch('src.services.flow_api.SystemMessage')
    @patch('src.services.flow_api.HumanMessage')
    async def test_generate_response_with_context(self, mock_human_message, mock_system_message, mock_chat_openai, mock_token_manager):
        """Tests generating a response with context"""
        # Arrange
        mock_token_manager_instance = AsyncMock()
        mock_token_manager_instance.get_valid_token.return_value = "test_token"
        mock_token_manager.return_value = mock_token_manager_instance
        
        mock_chat_model = MagicMock()
        mock_chat_openai.return_value = mock_chat_model
        
        mock_system_msg = MagicMock()
        mock_system_message.return_value = mock_system_msg
        
        mock_human_msg = MagicMock()
        mock_human_message.return_value = mock_human_msg
        
        mock_response = MagicMock()
        mock_response.content = "This is a test response with context"
        mock_chat_model.invoke.return_value = mock_response
        
        service = FlowAPIService()
        context_chunks = ["Chunk 1 about AI", "Chunk 2 about AI"]
        
        # Act
        result = await service.generate_response("What is AI?", context_chunks)
        
        # Assert
        assert result["status"] == "success"
        assert result["response"] == "This is a test response with context"
        mock_system_message.assert_called_once()
        mock_human_message.assert_called_once_with(content="What is AI?")
        mock_chat_model.invoke.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.services.flow_api.TokenManager')
    @patch('src.services.flow_api.ChatOpenAI')
    async def test_generate_response_exception(self, mock_chat_openai, mock_token_manager):
        """Tests exception handling in response generation"""
        # Arrange
        mock_token_manager_instance = AsyncMock()
        mock_token_manager_instance.get_valid_token.return_value = "test_token"
        mock_token_manager.return_value = mock_token_manager_instance
        
        mock_chat_model = MagicMock()
        mock_chat_openai.return_value = mock_chat_model
        mock_chat_model.invoke.side_effect = Exception("Test error")
        
        service = FlowAPIService()
        
        # Act
        result = await service.generate_response("What is AI?")
        
        # Assert
        assert result["status"] == "error"
        assert "Test error" in result["message"]