from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

class NavigationBar(QWidget):
    """Navigation bar for switching between different views"""

    view_changed = Signal(str)
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(60)
        self.setStyleSheet("""
    NavigationBar {
        background-color: #0d47a1;
    }
    QLabel {
        font-size: 16px;
        font-weight: bold;
        color: white;
    }
    QPushButton {
        background-color: transparent;
        color: white;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: #1565c0;
    }
    QPushButton:pressed {
        background-color: #1e88e5;
    }
    """)

        # Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(15)

        # Title
        title_label = QLabel("📊 Stock Market Analysis")
        main_layout.addWidget(title_label)

        # Spacer
        main_layout.addStretch(1)

        # Buttons
        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.clicked.connect(lambda: self.change_view("dashboard"))
        main_layout.addWidget(self.dashboard_button)

        self.chart_button = QPushButton("Charts")
        self.chart_button.clicked.connect(lambda: self.change_view("chart"))
        main_layout.addWidget(self.chart_button)

        self.portfolio_button = QPushButton("Portfolio")
        self.portfolio_button.clicked.connect(lambda: self.change_view("portfolio"))
        main_layout.addWidget(self.portfolio_button)

        self.advisor_button = QPushButton("AI Advisor")
        self.advisor_button.clicked.connect(lambda: self.change_view("advisor"))
        main_layout.addWidget(self.advisor_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_requested.emit)
        main_layout.addWidget(self.logout_button)

        # Store buttons for easy access
        self.buttons = {
            "dashboard": self.dashboard_button,
            "chart": self.chart_button,
            "portfolio": self.portfolio_button,
            "advisor": self.advisor_button
        }

    def change_view(self, view_name: str):
        self.set_active(view_name)
        self.view_changed.emit(view_name)

    def set_active(self, name: str):
        for key, btn in self.buttons.items():
            if key == name:
                btn.setStyleSheet("""
                    background-color: #1e88e5;
                    color: white;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 14px;
                """)
            else:
                btn.setStyleSheet("""
                    background-color: transparent;
                    color: white;
                    font-weight: normal;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 14px;
                """)
