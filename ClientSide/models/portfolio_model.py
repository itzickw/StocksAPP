from typing import Dict, List, Any, Optional
from utils.api_client import ApiClient

class PortfolioModel:
    """
    Model class for portfolio data
    Handles business logic related to user's stock portfolio
    """
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        
    def get_user_holdings(self, email: Optional[str] = None, password: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get user stock holdings using email and password"""
        return self.api_client.get_user_holdings(email, password)
    
    def get_user_transactions(self, email: Optional[str] = None, password: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get user transactions using email and password"""
        return self.api_client.get_user_transactions(email, password)
    
    def create_transaction(self, client_id: int, stock_symbol: str, quantity: float, transaction_type: str) -> Dict[str, Any]:
        """Create a new transaction using client ID"""
        # This method might still be valid if the API supports it
        return self.api_client.create_transaction(client_id, stock_symbol, quantity, transaction_type)
    
    def create_transaction_by_email(self, email: str, password: str, stock_symbol: str, 
                                   quantity: float, transaction_type: str) -> Dict[str, Any]:
        """Create a new transaction by email"""
        return self.api_client.create_transaction_by_email(email, password, stock_symbol, quantity, transaction_type)
