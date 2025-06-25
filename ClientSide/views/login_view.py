from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

class LoginView(QWidget):
    """Login view component for user authentication"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(self._style_sheet())
        self.setup_ui()
        

    def setup_ui(self):
        # === Main horizontal split layout ===
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Left panel (branding/info) ===
        left_widget = QWidget()
        left_widget.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.setSpacing(20)
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo.png")  # Optional: add your logo here
        # Resize the logo proportionally up to 180x180 max
        logo_size = 300
        scaled_logo = logo_pixmap.scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        logo_label.setAlignment(Qt.AlignCenter)
        # Optional: limit max height to keep it tidy
        logo_label.setMaximumHeight(logo_size)
        
        title_label = QLabel("Stock Market Analyzer")
        title_font = QFont("Poppins", 22, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #00BFFF;")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel("AI-powered insights\nTrack your investments\nVisual stock trends")
        subtitle_font = QFont("Poppins", 13)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #CCCCCC;")
        subtitle_label.setAlignment(Qt.AlignCenter)

        # Add to layout
        left_layout.addSpacing(10)        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(title_label)
        left_layout.addWidget(subtitle_label)
        left_layout.addStretch()

        # === Right panel (form) ===
        right_widget = QWidget()
        right_widget.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(20)

        form_title = QLabel("Login to your account")
        form_title.setFont(QFont("Poppins", 16, QFont.Bold))
        form_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(form_title)

        # Email
        email_layout = QVBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        right_layout.addLayout(email_layout)

        # Password
        password_layout = QVBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        right_layout.addLayout(password_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.register_button = QPushButton("Register")
        self.register_button.setMinimumHeight(40)
        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)
        right_layout.addLayout(buttons_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.status_label)

        # Tab order
        self.setTabOrder(self.email_input, self.password_input)
        self.setTabOrder(self.password_input, self.login_button)
        self.setTabOrder(self.login_button, self.register_button)

        # Focus
        self.email_input.setFocus()

        # Add panels to main layout
        main_layout.addWidget(left_widget, 2)
        main_layout.addWidget(right_widget, 1)

    def clear_inputs(self):
        """Clear input fields"""
        self.email_input.clear()
        self.password_input.clear()
        self.email_input.setFocus()

    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)

    def show_success(self, message):
        """Show success message"""
        QMessageBox.information(self, "Success", message)

    def _style_sheet(self):
        return """
        QWidget {
            background-color: #1e1e1e;
            font-family: 'Poppins', sans-serif;
            color: #FFFFFF;
        }
        #leftPanel {
            background-color: #1e1e1e;
        }
        #rightPanel {
            background-color: #1e1e1e;
        }
        QLineEdit {
            background-color: #2e2e2e;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 8px 12px;
            color: #DDDDDD;
        }
        QPushButton {
            background-color: #00BFFF;
            border: none;
            border-radius: 6px;
            padding: 10px 12px;
            font-weight: bold;
            color: white;
        }
        QPushButton:hover {
            background-color: #009ACD;
        }
        """
