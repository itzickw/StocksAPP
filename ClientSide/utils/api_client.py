import requests
import json
from typing import Dict, Any, Optional, List, Union

class ApiClient:
    """
    API Client for the Gateway API
    Handles all API requests to the gateway server
    """
    def __init__(self, base_url: str = "http://localhost:9000"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.user_email = None
        self.user_password = None # Note: Storing password in memory is not ideal for production
    
    def set_token(self, token: str):
        """Set authentication token after login"""
        self.token = token
    
    def set_user_credentials(self, email: str, password: str):
        """Set user credentials after login"""
        self.user_email = email
        self.user_password = password
    
    def set_user_id(self, user_id: str):
        """Set user ID after login"""
        self.user_id = user_id
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {
            "Content-Type": "application/json"
        }
        # Note: The API documentation doesn't explicitly mention bearer tokens for all endpoints.
        # If the /holding and /transactions endpoints don't require a token, this might need adjustment.
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API response and return data or raise exception"""
        if response.status_code >= 200 and response.status_code < 300:
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
        else:
            error_message = f"API Error: {response.status_code}"
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and "message" in error_data:
                    error_message = f"{error_message} - {error_data["message"]}"
                elif isinstance(error_data, str):
                     error_message = f"{error_message} - {error_data}"
            except:
                 error_message = f"{error_message} - {response.text}"
            raise Exception(error_message)
    
    # User API endpoints (V2 only)
    def register_user(self, email: str, password: str) -> Any:
        """Register a new user using V2 endpoint"""
        url = f"{self.base_url}/api/User/V2/Registration"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)
    
    def login_user(self, email: str, password: str) -> Any:
        """Login user using V2 endpoint"""
        url = f"{self.base_url}/api/User/V2/Login"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = self._handle_response(response)
        # Assuming the response contains token information
        if isinstance(result, dict) and "token" in result:
            self.set_token(result["token"])
        # Store credentials after successful login
        self.set_user_credentials(email, password)
        return result
    
    def get_user_id(self, email: str, password: str) -> Any:
        """Get user ID using V2 endpoint"""
        url = f"{self.base_url}/api/User/V2/UserId"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = self._handle_response(response)
        # Assuming the response contains user ID information
        if isinstance(result, dict) and "userId" in result:
            self.set_user_id(result["userId"])
        return result
    
    def update_password(self, email: str, password: str, new_password: str, new_email: Optional[str] = None) -> Any:
        """Update user password using V2 endpoint"""
        url = f"{self.base_url}/api/User/V2/UpdatePassword"
        data = {
            "email": email,
            "password": password,
            "newPassword": new_password
        }
        if new_email:
            data["newEmail"] = new_email
        response = requests.put(url, headers=self._get_headers(), json=data)
        # Update stored credentials if email changed
        if new_email:
            self.set_user_credentials(new_email, new_password)
        else:
            self.set_user_credentials(email, new_password)
        return self._handle_response(response)
    
    def delete_user(self, email: str, password: str) -> Any:
        """Delete user using V2 endpoint"""
        url = f"{self.base_url}/api/User/V2/DeleteUser"
        params = {
            "email": email,
            "password": password
        }
        response = requests.delete(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)
    
    # AIAdvisor API endpoints
    def get_ai_advice(self, query: str) -> Any:
        """Get AI advice based on query"""
        url = f"{self.base_url}/api/AIAdvisor/AIadvice/{query}"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_history_based_advice(self, stock_symbol: str) -> Any:
        """Get AI advice based on stock history"""
        url = f"{self.base_url}/api/AIAdvisor/based-history-advice/{stock_symbol}"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    # StockData API endpoints
    def get_current_stock_data(self, symbol: str) -> Any:
        """Get current stock data for a symbol"""
        url = f"{self.base_url}/api/StockData/current-data/{symbol}"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_stock_history(self, symbol: str, range_days: int) -> Any:
        """Get stock history for a symbol and range"""
        url = f"{self.base_url}/api/StockData/stock-history/{symbol}/{range_days}"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_stock_weekly_history(self, symbol: str, range_days: int, interval: int) -> Any:
        """Get stock weekly history for a symbol, range, and interval"""
        url = f"{self.base_url}/api/StockData/stock-weekly-history"
        params = {
            "symbol": symbol,
            "range": range_days,
            "interval": interval
        }
        response = requests.get(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)
    
    # StockManagement API endpoints
    def get_user_holdings(self, email: Optional[str] = None, password: Optional[str] = None) -> Any:
        """Get user stock holdings using email and password"""
        email = email or self.user_email
        password = password or self.user_password
        if not email or not password:
            raise ValueError("Email and password are required to fetch holdings")
        url = f"{self.base_url}/holding" # Use POST endpoint as requested
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)
    
    # Keep the old post_user_holdings method if it's for a different purpose (e.g., creation)
    # Renaming it to avoid confusion if needed, but based on the name, it seems redundant now.
    # def post_user_holdings(self, email: str, password: str) -> Any:
    #     """Post user holdings"""
    #     url = f"{self.base_url}/holding"
    #     data = {
    #         "email": email,
    #         "password": password
    #     }
    #     response = requests.post(url, headers=self._get_headers(), json=data)
    #     return self._handle_response(response)
    
    def get_user_transactions(self, email: Optional[str] = None, password: Optional[str] = None) -> Any:
        """Get user transactions using email and password"""
        email = email or self.user_email
        password = password or self.user_password
        if not email or not password:
            raise ValueError("Email and password are required to fetch transactions")
        url = f"{self.base_url}/transactions" # Use POST endpoint as requested
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)
    
    # Keep the old post_user_transactions method if it's for a different purpose.
    # def post_user_transactions(self, email: str, password: str) -> Any:
    #     """Post user transactions"""
    #     url = f"{self.base_url}/transactions"
    #     data = {
    #         "email": email,
    #         "password": password
    #     }
    #     response = requests.post(url, headers=self._get_headers(), json=data)
    #     return self._handle_response(response)
    
    def create_transaction(self, client_id: int, stock_symbol: str, quantity: float, transaction_type: str) -> Any:
        """Create a new transaction using client ID"""
        url = f"{self.base_url}/api/StockManagement/transaction"
        data = {
            "clientId": client_id,
            "stockSymbol": stock_symbol,
            "quantity": quantity,
            "transactionType": transaction_type
        }
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)
    
    def create_transaction_by_email(self, email: str, password: str, stock_symbol: str, 
                                   quantity: float, transaction_type: str) -> Any:
        """Create a new transaction by email"""
        url = f"{self.base_url}/api/StockManagement/transactionByEmail"
        data = {
            "email": email,
            "password": password,
            "stockSymbol": stock_symbol,
            "quantity": quantity,
            "transactionType": transaction_type
        }
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)
