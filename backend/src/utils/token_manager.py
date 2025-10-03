import os
import json
import time
import httpx
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from src.config.settings import settings

class TokenManager:
    """
    Manages the access token for the Flow API, checking its validity and updating it when necessary.
    """
    def __init__(self):
        self.token_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '.flow_token.json')
        self.client_id = settings.FLOW_CLIENT_ID
        self.client_secret = settings.FLOW_CLIENT_SECRET
        self.tenant = settings.FLOW_TENANT
        self.token_url = "https://flow.ciandt.com/auth-engine-api/v1/api-key/token"
        self.app_to_access = "llm-api"
        
        self.expiry_buffer = 300
    
    def _read_token_file(self) -> Optional[Dict[str, Any]]:
        """
        Reads the token file if it exists
        
        Returns:
            Dictionary with token data or None if file doesn't exist or is invalid
        """
        if not os.path.exists(self.token_file_path):
            return None
        
        try:
            with open(self.token_file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def _write_token_file(self, token_data: Dict[str, Any]) -> None:
        """
        Writes token data to a file
        
        Args:
            token_data: Dictionary containing token information
        """
        with open(self.token_file_path, 'w') as f:
            json.dump(token_data, f)
    
    def _is_token_valid(self, token_data: Dict[str, Any]) -> bool:
        """
        Checks if the token is still valid
        
        Args:
            token_data: Dictionary containing token information
            
        Returns:
            True if token is valid and not about to expire, False otherwise
        """
        if not token_data or 'access_token' not in token_data:
            return False
        
        try:
            token = token_data['access_token']
            decoded = jwt.decode(token, options={"verify_signature": False})
            
            exp_time = decoded.get('exp', 0)
            current_time = time.time()
            
            return exp_time > current_time + self.expiry_buffer
            
        except (jwt.PyJWTError, KeyError):
            return False
    
    async def _fetch_new_token(self) -> Dict[str, Any]:
        """
        Fetches a new access token from the API
        
        Returns:
            Dictionary containing the new token data
            
        Raises:
            Exception: If the API request fails
        """
        headers = {
            "accept": "/",
            "Content-Type": "application/json",
            "FlowTenant": self.tenant
        }
        
        payload = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "appToAccess": self.app_to_access
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.json()
    
    async def get_valid_token(self) -> str:
        """
        Returns a valid access token, renewing it if necessary
        
        Returns:
            String containing the access token
            
        Raises:
            Exception: If unable to obtain a valid token
        """
        token_data = self._read_token_file()
        
        if not self._is_token_valid(token_data):
            print("Token expired or invalid. Fetching new token...")
            try:
                token_data = await self._fetch_new_token()
                self._write_token_file(token_data)
                print("New token successfully obtained!")
            except Exception as e:
                print(f"Error fetching new token: {str(e)}")
                if token_data and 'access_token' in token_data:
                    print("Using existing token, even though it may be expired")
                else:
                    raise Exception("Could not obtain a valid token")
        
        return token_data['access_token']