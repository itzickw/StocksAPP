from typing import Dict, List, Any, Optional
from utils.api_client import ApiClient

class StockModel:
    """
    Model class for stock data
    Handles business logic related to stocks
    """
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        
    def get_current_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get current stock data for a symbol"""
        return self.api_client.get_current_stock_data(symbol)
    
    def get_stock_history(self, symbol: str, range_days: int) -> List[Dict[str, Any]]:
        """Get stock history for a symbol and range"""
        return self.api_client.get_stock_history(symbol, range_days)
    
    def get_stock_weekly_history(self, symbol: str, range_days: int, interval: int) -> List[Dict[str, Any]]:
        """Get stock weekly history for a symbol, range, and interval"""
        return self.api_client.get_stock_weekly_history(symbol, range_days, interval)
    
    def get_ai_advice(self, query: str) -> str:
        """Get AI advice based on query"""
        return self.api_client.get_ai_advice(query)
    
    def get_history_based_advice(self, stock_symbol: str) -> str:
        """Get AI advice based on stock history"""
        return self.api_client.get_history_based_advice(stock_symbol)
