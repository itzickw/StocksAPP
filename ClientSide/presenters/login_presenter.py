from PySide6.QtCore import QObject, Signal, Slot
from typing import Dict, Any

class LoginPresenter(QObject):
    """
    Presenter class for login view
    Handles the communication between login view and user model
    """
    
    login_successful = Signal()
    login_failed = Signal(str)
    registration_successful = Signal()
    registration_failed = Signal(str)
    
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        
        # Connect view signals to presenter slots
        self.view.login_requested.connect(self.login)
        self.view.register_requested.connect(self.register)
        
    @Slot(str, str)
    def login(self, email: str, password: str):
        """Handle login request"""
        try:
            result = self.model.login(email, password)
            if self.model.is_logged_in:
                self.login_successful.emit()
            else:
                error_message = "Login failed"
                if isinstance(result, dict) and "message" in result:
                    error_message = result["message"]
                self.login_failed.emit(error_message)
                self.view.show_error(error_message)
        except Exception as e:
            error_message = str(e)
            self.login_failed.emit(error_message)
            self.view.show_error(error_message)
    
    @Slot(str, str)
    def register(self, email: str, password: str):
        """Handle registration request"""
        try:
            result = self.model.register(email, password)
            if isinstance(result, dict) and result.get("success", False):
                self.registration_successful.emit()
                self.view.show_success("Registration successful. You can now login.")
                self.view.clear_fields()
            else:
                error_message = "Registration failed"
                if isinstance(result, dict) and "message" in result:
                    error_message = result["message"]
                self.registration_failed.emit(error_message)
                self.view.show_error(error_message)
        except Exception as e:
            error_message = str(e)
            self.registration_failed.emit(error_message)
            self.view.show_error(error_message)
