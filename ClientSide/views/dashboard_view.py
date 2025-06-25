from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QFrame, QMessageBox, QGridLayout
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis, QBarSeries, QBarSet, QBarCategoryAxis
import datetime

class DashboardView(QWidget):
    """Dashboard view component for displaying overview of market and portfolio"""
    
    refresh_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #1a1a1a;
            }
            QLabel[heading="true"] {
                font-size: 18px;
                font-weight: bold;
                color: #0d47a1;
                margin-bottom: 8px;
            }
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 8px 18px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("Market Dashboard")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Create splitter for top charts
        top_splitter = QSplitter(Qt.Horizontal)
        
        # Market overview chart
        market_chart_widget = QWidget()
        market_chart_layout = QVBoxLayout(market_chart_widget)
        market_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        market_chart_header = QLabel("Market Overview")
        market_chart_header.setProperty("heading", True)
        market_chart_header.setFont(QFont("Arial", 12, QFont.Bold))
        market_chart_layout.addWidget(market_chart_header)
        
        self.market_chart = QChart()
        self.market_chart.setTitle("Major Indices")
        self.market_chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.market_chart_view = QChartView(self.market_chart)
        self.market_chart_view.setRenderHint(QPainter.Antialiasing)
        market_chart_layout.addWidget(self.market_chart_view)
        
        top_splitter.addWidget(market_chart_widget)
        
        # Portfolio performance chart
        portfolio_chart_widget = QWidget()
        portfolio_chart_layout = QVBoxLayout(portfolio_chart_widget)
        portfolio_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        portfolio_chart_header = QLabel("Portfolio Performance")
        portfolio_chart_header.setFont(QFont("Arial", 12, QFont.Bold))
        portfolio_chart_layout.addWidget(portfolio_chart_header)
        
        self.portfolio_chart = QChart()
        self.portfolio_chart.setTitle("Portfolio Value Over Time")
        self.portfolio_chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.portfolio_chart_view = QChartView(self.portfolio_chart)
        self.portfolio_chart_view.setRenderHint(QPainter.Antialiasing)
        portfolio_chart_layout.addWidget(self.portfolio_chart_view)
        
        top_splitter.addWidget(portfolio_chart_widget)
        
        # Add top splitter to main layout
        main_layout.addWidget(top_splitter, 1)
        
        # Create splitter for bottom charts
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        # Top gainers chart
        gainers_chart_widget = QWidget()
        gainers_chart_layout = QVBoxLayout(gainers_chart_widget)
        gainers_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        gainers_chart_header = QLabel("Top Gainers")
        gainers_chart_header.setFont(QFont("Arial", 12, QFont.Bold))
        gainers_chart_layout.addWidget(gainers_chart_header)
        
        self.gainers_chart = QChart()
        self.gainers_chart.setTitle("Today's Top Performers")
        self.gainers_chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.gainers_chart_view = QChartView(self.gainers_chart)
        self.gainers_chart_view.setRenderHint(QPainter.Antialiasing)
        gainers_chart_layout.addWidget(self.gainers_chart_view)
        
        bottom_splitter.addWidget(gainers_chart_widget)
        
        # Top losers chart
        losers_chart_widget = QWidget()
        losers_chart_layout = QVBoxLayout(losers_chart_widget)
        losers_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        losers_chart_header = QLabel("Top Losers")
        losers_chart_header.setFont(QFont("Arial", 12, QFont.Bold))
        losers_chart_layout.addWidget(losers_chart_header)
        
        self.losers_chart = QChart()
        self.losers_chart.setTitle("Today's Worst Performers")
        self.losers_chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.losers_chart_view = QChartView(self.losers_chart)
        self.losers_chart_view.setRenderHint(QPainter.Antialiasing)
        losers_chart_layout.addWidget(self.losers_chart_view)
        
        bottom_splitter.addWidget(losers_chart_widget)
        
        # Add bottom splitter to main layout
        main_layout.addWidget(bottom_splitter, 1)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch(1)
        
        self.refresh_button = QPushButton("Refresh Dashboard")
        self.refresh_button.clicked.connect(self.refresh_requested.emit)
        refresh_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(refresh_layout)
        
    def update_market_chart(self, data):
        """Update market overview chart with indices data"""
        self.market_chart.removeAllSeries()
        
        # Create bar series
        series = QBarSeries()
        
        # Create bar sets for different indices
        indices = ["S&P 500", "NASDAQ", "DOW", "RUSSELL"]
        colors = [QColor(0, 128, 255), QColor(255, 128, 0), QColor(0, 192, 0), QColor(192, 0, 192)]
        
        for i, index_name in enumerate(indices):
            # Mock data for demonstration
            if not data or i >= len(data):
                value = (i + 1) * 0.5  # Mock percentage change
            else:
                value = data[i].get('change_percent', (i + 1) * 0.5)
                
            bar_set = QBarSet(index_name)
            bar_set.setColor(colors[i])
            bar_set.append(value)
            series.append(bar_set)
        
        self.market_chart.addSeries(series)
        
        # Create axes
        axis_x = QBarCategoryAxis()
        axis_x.append(["Daily Change %"])
        self.market_chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(-3, 3)  # Range for percentage change
        axis_y.setLabelFormat("%.1f%%")
        self.market_chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Set legend visibility
        self.market_chart.legend().setVisible(True)
        self.market_chart.legend().setAlignment(Qt.AlignBottom)
        
    def update_portfolio_chart(self, data):
        """Update portfolio performance chart with historical value data"""
        self.portfolio_chart.removeAllSeries()
        
        # Create line series
        series = QLineSeries()
        series.setName("Portfolio Value")
        
        # Add data points
        min_y = float('inf')
        max_y = float('-inf')
        min_x = float('inf')
        max_x = float('-inf')
        
        # Mock data for demonstration if no real data
        if not data or not isinstance(data, list):
            today = datetime.datetime.now()
            for i in range(30):
                date = today - datetime.timedelta(days=i)
                timestamp = date.timestamp() * 1000  # Convert to milliseconds
                value = 10000 + i * 100  # Mock portfolio value
                
                series.append(timestamp, value)
                
                min_y = min(min_y, value)
                max_y = max(max_y, value)
                min_x = min(min_x, timestamp)
                max_x = max(max_x, timestamp)
        else:
            for point in data:
                timestamp = datetime.datetime.fromisoformat(point['date']).timestamp() * 1000
                value = point['value']
                
                series.append(timestamp, value)
                
                min_y = min(min_y, value)
                max_y = max(max_y, value)
                min_x = min(min_x, timestamp)
                max_x = max(max_x, timestamp)
        
        self.portfolio_chart.addSeries(series)
        
        # Create X axis (time)
        axis_x = QDateTimeAxis()
        axis_x.setFormat("MMM dd")
        axis_x.setTitleText("Date")
        self.portfolio_chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        # Create Y axis (value)
        axis_y = QValueAxis()
        axis_y.setLabelFormat("$%.0f")
        axis_y.setTitleText("Portfolio Value")
        
        # Set range with some padding
        padding_y = (max_y - min_y) * 0.1
        axis_y.setRange(min_y - padding_y, max_y + padding_y)
        
        self.portfolio_chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Set X axis range
        axis_x.setRange(
            datetime.datetime.fromtimestamp(min_x / 1000),
            datetime.datetime.fromtimestamp(max_x / 1000)
        )
        
    def update_gainers_chart(self, data):
        """Update top gainers chart"""
        self.gainers_chart.removeAllSeries()
        
        # Create bar series
        series = QBarSeries()
        
        # Create bar set for gainers
        bar_set = QBarSet("% Gain")
        bar_set.setColor(QColor(0, 192, 0))  # Green for gainers
        
        # Categories for x-axis
        categories = []
        
        # Mock data for demonstration if no real data
        if not data or not isinstance(data, list):
            symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA"]
            values = [5.2, 4.8, 4.3, 3.9, 3.5]
            
            for value in values:
                bar_set.append(value)
                
            for symbol in symbols:
                categories.append(symbol)
        else:
            for item in data:
                bar_set.append(item['change_percent'])
                categories.append(item['symbol'])
        
        series.append(bar_set)
        self.gainers_chart.addSeries(series)
        
        # Create axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.gainers_chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 10)  # Range for percentage gain
        axis_y.setLabelFormat("%.1f%%")
        self.gainers_chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
    def update_losers_chart(self, data):
        """Update top losers chart"""
        self.losers_chart.removeAllSeries()
        
        # Create bar series
        series = QBarSeries()
        
        # Create bar set for losers
        bar_set = QBarSet("% Loss")
        bar_set.setColor(QColor(192, 0, 0))  # Red for losers
        
        # Categories for x-axis
        categories = []
        
        # Mock data for demonstration if no real data
        if not data or not isinstance(data, list):
            symbols = ["FB", "NFLX", "INTC", "AMD", "NVDA"]
            values = [-5.2, -4.8, -4.3, -3.9, -3.5]
            
            for value in values:
                bar_set.append(abs(value))  # Use absolute value for display
                
            for symbol in symbols:
                categories.append(symbol)
        else:
            for item in data:
                bar_set.append(abs(item['change_percent']))  # Use absolute value for display
                categories.append(item['symbol'])
        
        series.append(bar_set)
        self.losers_chart.addSeries(series)
        
        # Create axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.losers_chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 10)  # Range for percentage loss
        axis_y.setLabelFormat("%.1f%%")
        self.losers_chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
