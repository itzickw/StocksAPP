from PySide6.QtCore import QObject, Signal, Slot
from typing import Dict, Any

class StockChartPresenter(QObject):
    """
    Presenter class for stock chart view
    Handles the communication between stock chart view and stock model
    """
    
    chart_updated = Signal()
    chart_update_failed = Signal(str)
    
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        
        # Connect view signals to presenter slots
        self.view.refresh_button.clicked.connect(self.update_chart)
        self.view.symbol_combo.currentIndexChanged.connect(self.update_chart)
        self.view.range_combo.currentIndexChanged.connect(self.update_chart)
        self.view.chart_type_combo.currentIndexChanged.connect(self.update_chart)
        
        # Initial chart update
        self.update_chart()
        
    @Slot()
    def update_chart(self):
        """Update the chart with current settings"""
        try:
            symbol = self.view.symbol_combo.currentText()
            range_text = self.view.range_combo.currentText()
            chart_type = self.view.chart_type_combo.currentText()
            
            # Convert range text to days
            range_days = self._get_range_days(range_text)
            
            # Get stock history data with improved error handling
            try:
                stock_history = self.model.get_stock_history(symbol, range_days)
                
                # Check if we got valid data
                if not stock_history or not isinstance(stock_history, list):
                    self.view.show_error(f"No valid data received for {symbol}")
                    self.view.clear_chart()
                    return
                    
                # Process data for chart based on the new structure
                chart_data = self._process_data_for_chart(stock_history)
                
                # Update chart based on chart type
                if chart_type == "Line":
                    self.view.update_line_chart(chart_data)
                elif chart_type == "Candlestick":
                    # Candlestick chart requires OHLC data, which is not available from this endpoint
                    # Show an error or disable the option? For now, show line chart and inform user.
                    self.view.show_error("Candlestick chart requires OHLC data, which is not available from this endpoint. Displaying Line chart instead.")
                    self.view.update_line_chart(chart_data)
                
                self.chart_updated.emit()
                
            except Exception as e:
                error_message = str(e)
                self.chart_update_failed.emit(error_message)
                self.view.show_error(f"Failed to update chart: {error_message}")
                self.view.clear_chart()
                
        except Exception as e:
            error_message = str(e)
            self.chart_update_failed.emit(error_message)
            self.view.show_error(f"Failed to update chart: {error_message}")
            self.view.clear_chart()
    
    def _get_range_days(self, range_text: str) -> int:
        """Convert range text to number of days"""
        if range_text == "1 Day":
            return 1 # API might need adjustment for 1 day history
        elif range_text == "1 Week":
            return 7
        elif range_text == "1 Month":
            return 30
        elif range_text == "3 Months":
            return 90
        elif range_text == "6 Months":
            return 180
        elif range_text == "1 Year":
            return 365
        else:
            return 30  # Default to 1 month
    
    def _process_data_for_chart(self, stock_history: list) -> list:
        """Process stock history data (date, closePrice) for chart display"""
        processed_data = []
        
        if not stock_history or not isinstance(stock_history, list):
            # Handle empty or invalid data
            print("Warning: Received empty or invalid stock history data.")
            return []
        
        for item in stock_history:
            # Adapt to the actual API response structure: date, closePrice
            if not isinstance(item, dict):
                print(f"Warning: Skipping invalid data point: {item}")
                continue
                
            date_str = item.get("date")
            close_price = item.get("closePrice")
            
            if date_str is None or close_price is None:
                print(f"Warning: Skipping invalid data point: {item}")
                continue
                
            # Convert date string to datetime object if needed by chart view
            # Assuming chart view expects ISO format string for date
            processed_item = {
                "date": date_str, # Keep as string, chart view will handle parsing
                "price": float(close_price), # Use 'price' key for consistency in line chart view
                # OHLC data is not available
                "open": None,
                "high": None,
                "low": None,
                "close": float(close_price) # Keep close price if needed elsewhere
            }
            processed_data.append(processed_item)
            
        # Sort data by date ascending if necessary (API might already do this)
        processed_data.sort(key=lambda x: x["date"])
            
        return processed_data
