from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QMessageBox
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QPainter

class AIAdvisorView(QWidget):
    """AI Advisor view component for displaying AI-based stock advice"""
    
    advice_requested = Signal(str)
    history_advice_requested = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("AI Stock Advisor")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Description
        description_label = QLabel("Get AI-powered advice on stocks and investment strategies")
        description_font = QFont()
        description_font.setPointSize(10)
        description_label.setFont(description_font)
        main_layout.addWidget(description_label)
        
        # General advice section
        advice_section_label = QLabel("Ask for Investment Advice")
        advice_section_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(advice_section_label)
        
        # Query input
        query_layout = QHBoxLayout()
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter your investment question here...")
        self.query_button = QPushButton("Get Advice")
        self.query_button.clicked.connect(self.on_advice_requested)
        query_layout.addWidget(self.query_input, 1)
        query_layout.addWidget(self.query_button)
        main_layout.addLayout(query_layout)
        
        # Stock-specific advice section
        stock_advice_section_label = QLabel("Get Stock-Specific Advice")
        stock_advice_section_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(stock_advice_section_label)
        
        # Stock symbol input
        stock_layout = QHBoxLayout()
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Enter stock symbol (e.g., AAPL)")
        self.stock_button = QPushButton("Analyze Stock")
        self.stock_button.clicked.connect(self.on_history_advice_requested)
        stock_layout.addWidget(self.stock_input, 1)
        stock_layout.addWidget(self.stock_button)
        main_layout.addLayout(stock_layout)
        
        # Advice display
        advice_display_label = QLabel("AI Advice")
        advice_display_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(advice_display_label)
        
        self.advice_display = QTextEdit()
        self.advice_display.setReadOnly(True)
        self.advice_display.setMinimumHeight(300)
        main_layout.addWidget(self.advice_display, 1)
        
    def on_advice_requested(self):
        """Handle advice request button click"""
        query = self.query_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Error", "Please enter a question.")
            return
        
        self.advice_display.setText("Fetching advice...")
        self.advice_requested.emit(query)
        
    def on_history_advice_requested(self):
        """Handle stock history advice request button click"""
        symbol = self.stock_input.text().strip().upper()
        if not symbol:
            QMessageBox.warning(self, "Error", "Please enter a stock symbol.")
            return
        
        self.advice_display.setText(f"Analyzing {symbol}...")
        self.history_advice_requested.emit(symbol)
        
    def display_advice(self, advice):
        """Display AI advice"""
        self.advice_display.setText(advice)
        
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
        self.advice_display.setText("Error fetching advice. Please try again.")
