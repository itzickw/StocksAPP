from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QFrame, QMessageBox, QGridLayout
from PySide6.QtCore import Qt, Signal, Slot, QDateTime
from PySide6.QtGui import QFont, QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis, QCandlestickSeries, QCandlestickSet
import datetime

class StockChartView(QWidget):
    """Stock chart view component for displaying stock price charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Chart controls layout
        controls_layout = QHBoxLayout()
        
        # Symbol selection
        symbol_label = QLabel("Symbol:")
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"])
        self.symbol_combo.setMinimumWidth(100)
        controls_layout.addWidget(symbol_label)
        controls_layout.addWidget(self.symbol_combo)
        
        # Time range selection
        range_label = QLabel("Time Range:")
        self.range_combo = QComboBox()
        self.range_combo.addItems(["1 Day", "1 Week", "1 Month", "3 Months", "6 Months", "1 Year"])
        self.range_combo.setCurrentText("1 Month") # Default range
        self.range_combo.setMinimumWidth(100)
        controls_layout.addWidget(range_label)
        controls_layout.addWidget(self.range_combo)
        
        # Chart type selection
        chart_type_label = QLabel("Chart Type:")
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Line", "Candlestick"])
        self.chart_type_combo.setMinimumWidth(100)
        controls_layout.addWidget(chart_type_label)
        controls_layout.addWidget(self.chart_type_combo)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setMinimumWidth(80)
        controls_layout.addWidget(self.refresh_button)
        
        # Add controls to main layout
        main_layout.addLayout(controls_layout)
        
        # Create chart
        self.chart = QChart()
        self.chart.setTitle("Stock Price Chart")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        
        # Create chart view
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        # Add chart view to main layout
        main_layout.addWidget(self.chart_view)
        
    def update_line_chart(self, data):
        """Update the chart with line series data (using date string and price)"""
        # Clear existing series and axes
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
            
        if not data:
            self.chart.setTitle("No data available")
            return
            
        self.chart.setTitle(f"{self.symbol_combo.currentText()} Price Chart")
        
        # Create a line series
        series = QLineSeries()
        series.setName(f"{self.symbol_combo.currentText()} Price")
        
        # Add data points
        min_y = float("inf")
        max_y = float("-inf")
        min_x_dt = None
        max_x_dt = None
        
        for point in data:
            # Data format from presenter: {"date": "YYYY-MM-DDTHH:MM:SS", "price": float}
            date_str = point["date"]
            price = point["price"]
            
            # Convert ISO date string to QDateTime for the axis
            dt = QDateTime.fromString(date_str, Qt.ISODate)
            if not dt.isValid():
                print(f"Warning: Could not parse date string: {date_str}")
                continue
                
            timestamp_ms = dt.toMSecsSinceEpoch()
            series.append(timestamp_ms, price)
            
            min_y = min(min_y, price)
            max_y = max(max_y, price)
            
            if min_x_dt is None or dt < min_x_dt:
                min_x_dt = dt
            if max_x_dt is None or dt > max_x_dt:
                max_x_dt = dt
        
        if series.count() == 0:
             self.chart.setTitle("No valid data points found")
             return
             
        self.chart.addSeries(series)
        
        # Create X axis (time)
        axis_x = QDateTimeAxis()
        axis_x.setFormat("MMM dd yyyy") # Adjust format as needed
        axis_x.setTitleText("Date")
        # Set range based on actual data points
        if min_x_dt and max_x_dt:
            axis_x.setMin(min_x_dt)
            axis_x.setMax(max_x_dt)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        # Create Y axis (price)
        axis_y = QValueAxis()
        axis_y.setLabelFormat("$%.2f")
        axis_y.setTitleText("Price ($)")
        
        # Set range with some padding
        if min_y != float("inf") and max_y != float("-inf"):
            padding_y = (max_y - min_y) * 0.1 if max_y > min_y else 1.0
            axis_y.setMin(min_y - padding_y)
            axis_y.setMax(max_y + padding_y)
        else: # Handle case with single data point or no data
             axis_y.setMin(0)
             axis_y.setMax(100) # Default range
             
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
    def update_candlestick_chart(self, data):
        """Update the chart with candlestick series data (Placeholder - Not fully functional with current API)"""
        # Clear existing series and axes
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
            
        # Show message indicating data limitation
        self.chart.setTitle(f"{self.symbol_combo.currentText()} - Candlestick (Requires OHLC Data)")
        self.show_error("Candlestick chart requires Open, High, Low, Close (OHLC) data, which is not available from this API endpoint.")
        
        # Optionally, could try to display something basic or just leave it blank
        # For now, leave it blank after showing the error

    def show_error(self, message):
        """Show error message"""
        QMessageBox.warning(self, "Chart Error", message)
