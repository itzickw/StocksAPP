from typing import Dict, List, Any, Optional
from PySide6.QtCore import QObject, Signal, Slot

class UserModel(QObject):
    """
    User model class for handling user authentication and profile data
    """
    
    login_successful = Signal(dict)
    login_failed = Signal(str)
    registration_successful = Signal(dict)
    registration_failed = Signal(str)
    logout_successful = Signal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.is_logged_in = False
        self.user_data = {}
        
    def register(self, email: str, password: str):
        """Register a new user"""
        try:
            result = self.api_client.register_user(email, password)
            self.registration_successful.emit(result)
            return result
        except Exception as e:
            error_message = str(e)
            self.registration_failed.emit(error_message)
            raise
    
    def login(self, email: str, password: str):
        """Login user"""
        try:
            # ApiClient now validates login success and raises exception on failure
            result = self.api_client.login_user(email, password)
            
            # Check if login was successful based on API response
            if isinstance(result, dict) and result.get("success") == True:
                # Set login state based on successful API response
                self.is_logged_in = True
                
                # Store user data
                self.user_data = result
                self.login_successful.emit(result)
                return result
            else:
                # This should not happen as ApiClient should raise exception on failure
                # But handle it just in case
                error_message = "Login failed: Invalid response from server"
                self.is_logged_in = False
                self.login_failed.emit(error_message)
                raise Exception(error_message)
                
        except Exception as e:
            # Set login state to false on any exception
            self.is_logged_in = False
            error_message = str(e)
            self.login_failed.emit(error_message)
            raise
    
    def logout(self):
        """Logout user"""
        try:
            # Clear credentials in API client
            self.api_client.logout_user()
            
            # Reset login state
            self.is_logged_in = False
            self.user_data = {}
            
            self.logout_successful.emit()
            return True
        except Exception as e:
            # Even if API logout fails, we still want to clear local state
            self.is_logged_in = False
            self.user_data = {}
            self.logout_successful.emit()
            return True
    
    def update_password(self, current_password: str, new_password: str, new_email: Optional[str] = None):
        """Update user password"""
        try:
            if not self.is_logged_in or not self.api_client.user_email:
                raise Exception("User not logged in")
                
            result = self.api_client.update_password(
                self.api_client.user_email,
                current_password,
                new_password,
                new_email
            )
            return result
        except Exception as e:
            raise
    
    def delete_account(self, password: str):
        """Delete user account"""
        try:
            if not self.is_logged_in or not self.api_client.user_email:
                raise Exception("User not logged in")
                
            result = self.api_client.delete_user(self.api_client.user_email, password)
            
            # Reset login state after account deletion
            self.is_logged_in = False
            self.user_data = {}
            
            return result
        except Exception as e:
            raise
