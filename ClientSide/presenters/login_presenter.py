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
        self.view.login_button.clicked.connect(self.login)
        self.view.register_button.clicked.connect(self.register)
        
        # Connect model signals to presenter slots
        self.model.login_successful.connect(self.on_login_successful)
        self.model.login_failed.connect(self.on_login_failed)
        self.model.registration_successful.connect(self.on_registration_successful)
        self.model.registration_failed.connect(self.on_registration_failed)
        
    @Slot()
    def login(self):
        """Handle login button click"""
        email = self.view.email_input.text().strip()
        password = self.view.password_input.text()
        
        if not email:
            self.view.show_error("Please enter your email")
            return
        
        if not password:
            self.view.show_error("Please enter your password")
            return
        
        try:
            self.model.login(email, password)
        except Exception as e:
            # Error will be handled by on_login_failed via signal
            pass
    
    @Slot()
    def register(self):
        """Handle register button click"""
        email = self.view.email_input.text().strip()
        password = self.view.password_input.text()
        
        if not email:
            self.view.show_error("Please enter your email")
            return
        
        if not password:
            self.view.show_error("Please enter your password")
            return
        
        try:
            self.model.register(email, password)
        except Exception as e:
            # Error will be handled by on_registration_failed via signal
            pass
    
    @Slot(dict)
    def on_login_successful(self, user_data: Dict[str, Any]):
        """Handle successful login"""
        self.view.clear_inputs()
        self.login_successful.emit()
    
    @Slot(str)
    def on_login_failed(self, error_message: str):
        """Handle failed login"""
        self.view.show_error(f"Login failed: {error_message}")
    
    @Slot(dict)
    def on_registration_successful(self, user_data: Dict[str, Any]):
        """Handle successful registration"""
        self.view.clear_inputs()
        self.view.show_success("Registration successful! You can now log in.")
        self.registration_successful.emit()
    
    @Slot(str)
    def on_registration_failed(self, error_message: str):
        """Handle failed registration"""
        self.view.show_error(f"Registration failed: {error_message}")
