from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

class NavigationBar(QWidget):
    """Navigation bar for switching between different views"""
    
    view_changed = Signal(str)
    logout_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Create main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(10)
        
        # App title
        title_label = QLabel("Stock Market Analysis")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(title_label)
        
        # Add spacer
        main_layout.addStretch(1)
        
        # Dashboard button
        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.clicked.connect(lambda: self.view_changed.emit("dashboard"))
        main_layout.addWidget(self.dashboard_button)
        
        # Chart button
        self.chart_button = QPushButton("Charts")
        self.chart_button.clicked.connect(lambda: self.view_changed.emit("chart"))
        main_layout.addWidget(self.chart_button)
        
        # Portfolio button
        self.portfolio_button = QPushButton("Portfolio")
        self.portfolio_button.clicked.connect(lambda: self.view_changed.emit("portfolio"))
        main_layout.addWidget(self.portfolio_button)
        
        # AI Advisor button
        self.advisor_button = QPushButton("AI Advisor")
        self.advisor_button.clicked.connect(lambda: self.view_changed.emit("advisor"))
        main_layout.addWidget(self.advisor_button)
        
        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_requested.emit)
        main_layout.addWidget(self.logout_button)
