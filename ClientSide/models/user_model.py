from typing import Dict, List, Any, Optional
from utils.api_client import ApiClient

class UserModel:
    """
    Model class for user data
    Handles business logic related to user authentication and management
    """
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.is_logged_in = False
        self.user_email = None
        self.user_id = None
        
    def register(self, email: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        result = self.api_client.register_user(email, password)
        return result
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        result = self.api_client.login_user(email, password)
        if result and isinstance(result, dict):
            self.is_logged_in = True
            self.user_email = email
            # Get user ID
            user_id_result = self.api_client.get_user_id(email, password)
            if user_id_result and isinstance(user_id_result, dict) and "userId" in user_id_result:
                self.user_id = user_id_result["userId"]
                self.api_client.set_user_id(self.user_id)
        return result
    
    def logout(self) -> None:
        """Logout user"""
        self.is_logged_in = False
        self.user_email = None
        self.user_id = None
        self.api_client.set_token(None)
        self.api_client.set_user_id(None)
    
    def update_password(self, current_password: str, new_password: str, new_email: Optional[str] = None) -> Dict[str, Any]:
        """Update user password"""
        if not self.is_logged_in or not self.user_email:
            raise ValueError("User must be logged in to update password")
        result = self.api_client.update_password(self.user_email, current_password, new_password, new_email)
        if new_email:
            self.user_email = new_email
        return result
    
    def delete_account(self, password: str) -> Dict[str, Any]:
        """Delete user account"""
        if not self.is_logged_in or not self.user_email:
            raise ValueError("User must be logged in to delete account")
        result = self.api_client.delete_user(self.user_email, password)
        self.logout()
        return result
