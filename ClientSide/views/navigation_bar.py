from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap


class NavigationBar(QWidget):
    """Top navigation bar with buttons"""

    view_changed = Signal(str)
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = {}
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(30)

        layout.addStretch()  # Push buttons to center

        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo.png")  # Optional: add your logo here
        # Resize the logo proportionally up to 180x180 max
        logo_size = 45
        scaled_logo = logo_pixmap.scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        logo_label.setAlignment(Qt.AlignCenter)
        # Optional: limit max height to keep it tidy
        logo_label.setMaximumHeight(logo_size)
        logo_label.setStyleSheet("margin-right: 40px;")  # Add some margin to the right
        layout.addWidget(logo_label)
        
        # Create navigation buttons
        buttons_info = [
            ("Dashboard", "dashboard"),
            ("Chart", "chart"),
            ("Portfolio", "portfolio"),
            ("Advisor", "advisor"),
        ]

        for name, key in buttons_info:
            button = QPushButton(name)
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setMinimumWidth(120)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #1abc9c;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
            """)
            self.buttons[key] = button
            button.clicked.connect(lambda checked, k=key: self.emit_view_changed(k))
            layout.addWidget(button)

        layout.addSpacing(50)  # Space between nav buttons and logout

        # Add logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setCursor(Qt.PointingHandCursor)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        self.logout_button.clicked.connect(self.logout_requested.emit)
        layout.addWidget(self.logout_button)

        layout.addStretch()  # Push everything to center
        self.setLayout(layout)
        self.setStyleSheet("background-color: #2c3e50;")

    def emit_view_changed(self, view_key):
        self.set_active_button(view_key)
        self.view_changed.emit(view_key)

    def set_active_button(self, active_key):
        for key, button in self.buttons.items():
            button.setChecked(key == active_key)
            
    def set_active_view(self, view_key):
        """External call to set the active button"""
        self.set_active_button(view_key)

    def clear_selection(self):
        """Clear all button selections"""
        for button in self.buttons.values():
            button.setChecked(False)

