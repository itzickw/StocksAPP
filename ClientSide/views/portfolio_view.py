from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QMessageBox, QGridLayout, QComboBox, QDoubleSpinBox, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPainter
from PySide6.QtCharts import QChart, QChartView, QPieSeries

class PortfolioView(QWidget):
    """Portfolio view component for displaying user's stock holdings and transactions"""

    buy_stock_requested = Signal(str, float)
    sell_stock_requested = Signal(str, float)
    refresh_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Segoe UI', sans-serif;
            }
            QTableWidget, QHeaderView::section {
                background-color: #2c2c2c;
                color: #e0e0e0;
                gridline-color: #444;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #2c2c2c;
            }
            QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                padding: 6px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005fa1;
            }
        """)

        # Header row with title and refresh button
        header_layout = QHBoxLayout()
        title_label = QLabel("Portfolio Management")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        self.refresh_button.setFixedWidth(100)
        header_layout.addWidget(self.refresh_button)
        main_layout.addLayout(header_layout)

        # Main horizontal layout for tables and chart
        body_layout = QHBoxLayout()

        # Left side - Tables
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(20)

        # Portfolio table
        portfolio_header = QLabel("Current Holdings")
        portfolio_font = QFont()
        portfolio_font.setPointSize(12)
        portfolio_font.setBold(True)
        portfolio_header.setFont(portfolio_font)
        left_layout.addWidget(portfolio_header)

        self.portfolio_table = QTableWidget()
        self.portfolio_table.setColumnCount(5)
        self.portfolio_table.setHorizontalHeaderLabels(["Symbol", "Quantity", "Avg. Price", "Current Price", "Total Value"])
        self.portfolio_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.portfolio_table)

        # Transactions table
        transactions_header = QLabel("Transaction History")
        transactions_font = QFont()
        transactions_font.setPointSize(12)
        transactions_font.setBold(True)
        transactions_header.setFont(transactions_font)
        left_layout.addWidget(transactions_header)

        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["Date", "Symbol", "Type", "Quantity", "Price"])
        self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.transactions_table)

        # Right side - Pie chart
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(15)

        chart_header = QLabel("Portfolio Allocation by Value")
        chart_font = QFont()
        chart_font.setPointSize(12)
        chart_font.setBold(True)
        chart_header.setFont(chart_font)
        right_layout.addWidget(chart_header)

        self.portfolio_chart = QChart()
        self.portfolio_chart.setTitle("Portfolio Allocation")
        self.portfolio_chart.legend().setVisible(True)
        self.portfolio_chart.legend().setAlignment(Qt.AlignBottom)
        self.portfolio_chart_view = QChartView(self.portfolio_chart)
        self.portfolio_chart_view.setRenderHint(QPainter.Antialiasing)
        right_layout.addWidget(self.portfolio_chart_view)

        body_layout.addWidget(left_widget, 3)
        body_layout.addWidget(right_widget, 2)
        main_layout.addLayout(body_layout)

        # Bottom transaction controls
        bottom_section_label = QLabel("Stock Transactions")
        bottom_section_font = QFont()
        bottom_section_font.setPointSize(12)
        bottom_section_font.setBold(True)
        bottom_section_label.setFont(bottom_section_font)
        main_layout.addWidget(bottom_section_label)

        transaction_controls_layout = QHBoxLayout()
        
        symbol_label = QLabel("Symbol:")
        self.symbol_combo = QComboBox()
        self.symbol_combo.setEditable(True)
        self.symbol_combo.addItems(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"])
        self.symbol_combo.setFixedWidth(120)
        symbol_box = QHBoxLayout()
        symbol_box.setSpacing(2)    
        symbol_box.addWidget(symbol_label)
        symbol_box.addWidget(self.symbol_combo)
        
        quantity_box = QHBoxLayout()
        quantity_box.setSpacing(2)
        quantity_label = QLabel("Quantity:")
        self.quantity_spin = QDoubleSpinBox()
        self.quantity_spin.setMinimum(0.01)
        self.quantity_spin.setMaximum(10000)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setDecimals(2)
        self.quantity_spin.setFixedWidth(100)
        quantity_box.addWidget(quantity_label)
        quantity_box.addWidget(self.quantity_spin)
        
        self.buy_button = QPushButton("Buy")
        self.buy_button.clicked.connect(self.on_buy_clicked)
        self.sell_button = QPushButton("Sell")
        self.sell_button.clicked.connect(self.on_sell_clicked)

        field_layout = QHBoxLayout()
        field_layout.addLayout(symbol_box)
        field_layout.addLayout(quantity_box)
        field_layout.setSpacing(150)
        field_layout.addWidget(self.buy_button)
        field_layout.addWidget(self.sell_button)

        main_layout.addLayout(field_layout)

    def update_portfolio(self, holdings, total_portfolio_value):
        """Update the portfolio table and chart"""
        self.portfolio_table.setRowCount(0)
        pie_series = QPieSeries()

        if not isinstance(holdings, list):
            self.show_error("Invalid holdings data received.")
            holdings = []

        for i, holding in enumerate(holdings):
            self.portfolio_table.insertRow(i)
            symbol = holding.get('stockSymbol', 'N/A')
            quantity = holding.get('quantity', 0.0)
            avg_price = holding.get('avg_price', 0.0)
            current_price = holding.get('current_price', 0.0)
            total_value = holding.get('total_value', 0.0)

            self.portfolio_table.setItem(i, 0, QTableWidgetItem(symbol))
            self.portfolio_table.setItem(i, 1, QTableWidgetItem(f"{quantity:.2f}"))
            self.portfolio_table.setItem(i, 2, QTableWidgetItem(f"${avg_price:.2f}"))
            self.portfolio_table.setItem(i, 3, QTableWidgetItem(f"${current_price:.2f}"))
            self.portfolio_table.setItem(i, 4, QTableWidgetItem(f"${total_value:.2f}"))

            if total_value > 0:
                pie_series.append(symbol, total_value)

        self.portfolio_chart.removeAllSeries()
        self.portfolio_chart.addSeries(pie_series)

    def update_transactions(self, transactions):
        """Update the transactions table"""
        self.transactions_table.setRowCount(0)

        if not isinstance(transactions, list):
            self.show_error("Invalid transactions data received.")
            transactions = []

        for i, t in enumerate(transactions):
            self.transactions_table.insertRow(i)
            self.transactions_table.setItem(i, 0, QTableWidgetItem(t.get('date', 'N/A')))
            self.transactions_table.setItem(i, 1, QTableWidgetItem(t.get('stockSymbol', 'N/A')))
            self.transactions_table.setItem(i, 2, QTableWidgetItem(t.get('transactionType', 'N/A')))
            self.transactions_table.setItem(i, 3, QTableWidgetItem(f"{t.get('quantity', 0.0):.2f}"))
            self.transactions_table.setItem(i, 4, QTableWidgetItem(f"${t.get('price', 0.0):.2f}"))

    def on_refresh_clicked(self):
        """Emit signal to refresh portfolio"""
        self.refresh_requested.emit()

    def on_buy_clicked(self):
        """Emit signal to buy stock"""
        symbol = self.symbol_combo.currentText().strip().upper()
        quantity = self.quantity_spin.value()

        if not symbol:
            QMessageBox.warning(self, "Error", "Please enter a stock symbol.")
            return
        if quantity <= 0:
            QMessageBox.warning(self, "Error", "Please enter a valid quantity.")
            return

        self.buy_stock_requested.emit(symbol, quantity)

    def on_sell_clicked(self):
        """Emit signal to sell stock"""
        symbol = self.symbol_combo.currentText().strip().upper()
        quantity = self.quantity_spin.value()

        if not symbol:
            QMessageBox.warning(self, "Error", "Please enter a stock symbol.")
            return
        if quantity <= 0:
            QMessageBox.warning(self, "Error", "Please enter a valid quantity.")
            return

        self.sell_stock_requested.emit(symbol, quantity)

    def show_error(self, message):
        """Display error message"""
        QMessageBox.critical(self, "Error", message)

    def show_success(self, message):
        """Display success message"""
        QMessageBox.information(self, "Success", message)
