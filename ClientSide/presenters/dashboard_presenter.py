from PySide6.QtCore import QObject, Signal, Slot
from typing import Dict, Any, List

class DashboardPresenter(QObject):
    """
    Presenter class for dashboard view
    Handles the communication between dashboard view and models
    """
    
    dashboard_updated = Signal()
    dashboard_update_failed = Signal(str)
    
    def __init__(self, view, stock_model, portfolio_model):
        super().__init__()
        self.view = view
        self.stock_model = stock_model
        self.portfolio_model = portfolio_model
        
        # Connect view signals to presenter slots
        self.view.refresh_requested.connect(self.update_dashboard)
        
        # Initial dashboard update
        self.update_dashboard()
        
    @Slot()
    def update_dashboard(self):
        """Update all dashboard charts"""
        try:
            # Update market chart
            market_data = self._get_market_data()
            self.view.update_market_chart(market_data)
            
            # Update portfolio chart
            portfolio_data = self._get_portfolio_data()
            self.view.update_portfolio_chart(portfolio_data)
            
            # Update gainers chart
            gainers_data = self._get_gainers_data()
            self.view.update_gainers_chart(gainers_data)
            
            # Update losers chart
            losers_data = self._get_losers_data()
            self.view.update_losers_chart(losers_data)
            
            self.dashboard_updated.emit()
            
        except Exception as e:
            error_message = str(e)
            self.dashboard_update_failed.emit(error_message)
            # We don't show error in view here as it might be disruptive during initial load
    
    def _get_market_data(self):
        """Get market indices data"""
        # This would normally fetch data from the API
        # For demonstration, we'll use mock data
        return [
            {"index": "S&P 500", "value": 4200.5, "change_percent": 0.8},
            {"index": "NASDAQ", "value": 14100.2, "change_percent": 1.2},
            {"index": "DOW", "value": 34500.7, "change_percent": 0.5},
            {"index": "RUSSELL", "value": 2300.1, "change_percent": -0.3}
        ]
    
    def _get_portfolio_data(self):
        """Get portfolio historical data"""
        # This would normally fetch data from the API
        # For demonstration, we'll use mock data
        import datetime
        
        today = datetime.datetime.now()
        data = []
        
        for i in range(30):
            date = today - datetime.timedelta(days=i)
            value = 10000 + (30 - i) * 100  # Simple increasing value
            
            data.append({
                "date": date.isoformat(),
                "value": value
            })
            
        return data
    
    def _get_gainers_data(self):
        """Get top gainers data"""
        # This would normally fetch data from the API
        # For demonstration, we'll use mock data
        return [
            {"symbol": "AAPL", "price": 150.25, "change_percent": 5.2},
            {"symbol": "MSFT", "price": 290.50, "change_percent": 4.8},
            {"symbol": "AMZN", "price": 3400.75, "change_percent": 4.3},
            {"symbol": "GOOGL", "price": 2800.30, "change_percent": 3.9},
            {"symbol": "TSLA", "price": 750.80, "change_percent": 3.5}
        ]
    
    def _get_losers_data(self):
        """Get top losers data"""
        # This would normally fetch data from the API
        # For demonstration, we'll use mock data
        return [
            {"symbol": "META", "price": 320.15, "change_percent": -5.2},
            {"symbol": "NFLX", "price": 550.40, "change_percent": -4.8},
            {"symbol": "INTC", "price": 45.60, "change_percent": -4.3},
            {"symbol": "AMD", "price": 110.25, "change_percent": -3.9},
            {"symbol": "NVDA", "price": 220.70, "change_percent": -3.5}
        ]
