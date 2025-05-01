from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QFrame, QMessageBox, QGridLayout, QComboBox, QLineEdit, QDoubleSpinBox
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QPainter
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice

class PortfolioView(QWidget):
    """Portfolio view component for displaying user's stock holdings and transactions"""
    
    buy_stock_requested = Signal(str, float)
    sell_stock_requested = Signal(str, float)
    refresh_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("Portfolio Management")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Create splitter for portfolio and transactions
        splitter = QSplitter(Qt.Vertical)
        
        # Portfolio section
        portfolio_widget = QWidget()
        portfolio_layout = QVBoxLayout(portfolio_widget)
        portfolio_layout.setContentsMargins(0, 0, 0, 0)
        
        # Portfolio header
        portfolio_header = QLabel("Current Holdings")
        portfolio_header.setFont(QFont("Arial", 12, QFont.Bold))
        portfolio_layout.addWidget(portfolio_header)
        
        # Portfolio table
        self.portfolio_table = QTableWidget()
        self.portfolio_table.setColumnCount(5)
        # Updated headers to reflect available data + placeholders
        self.portfolio_table.setHorizontalHeaderLabels(["Symbol", "Quantity", "Avg. Price", "Current Price", "Total Value"])
        self.portfolio_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        portfolio_layout.addWidget(self.portfolio_table)
        
        # Portfolio summary
        portfolio_summary_layout = QHBoxLayout()
        
        # Portfolio value (will be updated with calculated value)
        self.portfolio_value_label = QLabel("Total Portfolio Value: $0.00")
        self.portfolio_value_label.setFont(QFont("Arial", 12, QFont.Bold))
        portfolio_summary_layout.addWidget(self.portfolio_value_label)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        portfolio_summary_layout.addWidget(self.refresh_button)
        
        portfolio_layout.addLayout(portfolio_summary_layout)
        
        # Add portfolio widget to splitter
        splitter.addWidget(portfolio_widget)
        
        # Portfolio chart widget
        portfolio_chart_widget = QWidget()
        portfolio_chart_layout = QVBoxLayout(portfolio_chart_widget)
        portfolio_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        # Portfolio chart header
        portfolio_chart_header = QLabel("Portfolio Allocation by Value") # Changed title back
        portfolio_chart_header.setFont(QFont("Arial", 12, QFont.Bold))
        portfolio_chart_layout.addWidget(portfolio_chart_header)
        
        # Create pie chart
        self.portfolio_chart = QChart()
        self.portfolio_chart.setTitle("Portfolio Allocation by Value") # Changed title back
        self.portfolio_chart.legend().setVisible(True)
        self.portfolio_chart.legend().setAlignment(Qt.AlignRight)
        
        # Create chart view
        self.portfolio_chart_view = QChartView(self.portfolio_chart)
        self.portfolio_chart_view.setRenderHint(QPainter.Antialiasing)
        portfolio_chart_layout.addWidget(self.portfolio_chart_view)
        
        # Add portfolio chart widget to splitter
        splitter.addWidget(portfolio_chart_widget)
        
        # Transactions section
        transactions_widget = QWidget()
        transactions_layout = QVBoxLayout(transactions_widget)
        transactions_layout.setContentsMargins(0, 0, 0, 0)
        
        # Transactions header
        transactions_header = QLabel("Transaction History")
        transactions_header.setFont(QFont("Arial", 12, QFont.Bold))
        transactions_layout.addWidget(transactions_header)
        
        # Transactions table
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["Date", "Symbol", "Type", "Quantity", "Price"])
        self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        transactions_layout.addWidget(self.transactions_table)
        
        # Add transactions widget to splitter
        splitter.addWidget(transactions_widget)
        
        # Add splitter to main layout
        main_layout.addWidget(splitter, 1)
        
        # Transaction controls
        transaction_controls_widget = QWidget()
        transaction_controls_layout = QGridLayout(transaction_controls_widget)
        
        # Stock symbol
        symbol_label = QLabel("Symbol:")
        self.symbol_combo = QComboBox()
        self.symbol_combo.setEditable(True)
        self.symbol_combo.addItems(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"])
        transaction_controls_layout.addWidget(symbol_label, 0, 0)
        transaction_controls_layout.addWidget(self.symbol_combo, 0, 1)
        
        # Quantity
        quantity_label = QLabel("Quantity:")
        self.quantity_spin = QDoubleSpinBox()
        self.quantity_spin.setMinimum(0.01)
        self.quantity_spin.setMaximum(10000)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setDecimals(2)
        transaction_controls_layout.addWidget(quantity_label, 0, 2)
        transaction_controls_layout.addWidget(self.quantity_spin, 0, 3)
        
        # Buy/Sell buttons
        self.buy_button = QPushButton("Buy")
        self.buy_button.clicked.connect(self.on_buy_clicked)
        self.sell_button = QPushButton("Sell")
        self.sell_button.clicked.connect(self.on_sell_clicked)
        transaction_controls_layout.addWidget(self.buy_button, 0, 4)
        transaction_controls_layout.addWidget(self.sell_button, 0, 5)
        
        main_layout.addWidget(transaction_controls_widget)
        
    # Modified to accept total_portfolio_value
    def update_portfolio(self, holdings, total_portfolio_value):
        """Update the portfolio table and chart with enriched holdings data"""
        self.portfolio_table.setRowCount(0)
        
        pie_series = QPieSeries()
        
        # Check if holdings is a list
        if not isinstance(holdings, list):
            self.show_error("Invalid holdings data received.")
            holdings = [] # Prevent further errors
            
        for i, holding in enumerate(holdings):
            self.portfolio_table.insertRow(i)
            
            # Use the enriched data structure from presenter
            symbol = holding.get('stockSymbol', 'N/A')
            quantity = holding.get('quantity', 0.0)
            avg_price = holding.get('avg_price', 0.0) # Use avg_price if available
            current_price = holding.get('current_price', 0.0)
            total_value_item = holding.get('total_value', 0.0)
            
            # Format data for display
            avg_price_str = f"${avg_price:.2f}" if avg_price else "N/A"
            current_price_str = f"${current_price:.2f}" if current_price else "N/A"
            total_value_item_str = f"${total_value_item:.2f}"
            
            self.portfolio_table.setItem(i, 0, QTableWidgetItem(symbol))
            self.portfolio_table.setItem(i, 1, QTableWidgetItem(f"{quantity:.2f}"))
            self.portfolio_table.setItem(i, 2, QTableWidgetItem(avg_price_str))
            self.portfolio_table.setItem(i, 3, QTableWidgetItem(current_price_str))
            self.portfolio_table.setItem(i, 4, QTableWidgetItem(total_value_item_str))
            
            # Add to pie chart based on value
            if total_value_item > 0:
                slice = pie_series.append(symbol, total_value_item)
                slice.setLabelVisible(True)
                # Label shows value and percentage of total value
                # Defer calculating percentage until total_portfolio_value is known

        # Update total portfolio value label
        self.portfolio_value_label.setText(f"Total Portfolio Value: ${total_portfolio_value:.2f}")
        
        # Update pie chart labels with percentages
        if total_portfolio_value > 0:
            for slice in pie_series.slices():
                label = slice.label()
                value = slice.value()
                percentage = (value / total_portfolio_value * 100) if total_portfolio_value else 0
                slice.setLabel(f"{label}: ${value:.2f} ({percentage:.1f}%) ")
        else:
             # Handle case where total value is zero or negative
             pie_series.clear()

        self.portfolio_chart.removeAllSeries()
        self.portfolio_chart.addSeries(pie_series)
        
    def update_transactions(self, transactions):
        """Update the transactions table with transaction data"""
        self.transactions_table.setRowCount(0)
        
        # Check if transactions is a list
        if not isinstance(transactions, list):
            self.show_error("Invalid transactions data received.")
            transactions = [] # Prevent further errors
            
        for i, transaction in enumerate(transactions):
            self.transactions_table.insertRow(i)
            
            # Assuming transaction is a dictionary with date, symbol, type, quantity, price keys
            # Adjust keys if the actual transaction data structure is different
            date = transaction.get('date', 'N/A') 
            symbol = transaction.get('stockSymbol', 'N/A') # Assuming same key as holdings
            transaction_type = transaction.get('transactionType', 'N/A') # Assuming this key
            quantity = transaction.get('quantity', 0.0)
            price = transaction.get('price', 0.0) # Assuming this key
            
            self.transactions_table.setItem(i, 0, QTableWidgetItem(str(date)))
            self.transactions_table.setItem(i, 1, QTableWidgetItem(symbol))
            self.transactions_table.setItem(i, 2, QTableWidgetItem(transaction_type))
            self.transactions_table.setItem(i, 3, QTableWidgetItem(f"{quantity:.2f}"))
            self.transactions_table.setItem(i, 4, QTableWidgetItem(f"${price:.2f}"))
    
    def on_buy_clicked(self):
        """Handle buy button click"""
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
        """Handle sell button click"""
        symbol = self.symbol_combo.currentText().strip().upper()
        quantity = self.quantity_spin.value()
        
        if not symbol:
            QMessageBox.warning(self, "Error", "Please enter a stock symbol.")
            return
        
        if quantity <= 0:
            QMessageBox.warning(self, "Error", "Please enter a valid quantity.")
            return
        
        self.sell_stock_requested.emit(symbol, quantity)
    
    def on_refresh_clicked(self):
        """Handle refresh button click"""
        self.refresh_requested.emit()
        
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
        
    def show_success(self, message):
        """Show success message"""
        QMessageBox.information(self, "Success", message)
