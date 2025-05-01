from PySide6.QtCore import QObject, Signal, Slot
from typing import Dict, Any, List

class PortfolioPresenter(QObject):
    """
    Presenter class for portfolio view
    Handles the communication between portfolio view and portfolio model
    """
    
    portfolio_updated = Signal()
    portfolio_update_failed = Signal(str)
    transaction_successful = Signal()
    transaction_failed = Signal(str)
    
    def __init__(self, view, model, user_model):
        super().__init__()
        self.view = view
        self.model = model # PortfolioModel
        self.user_model = user_model # UserModel
        # Need access to StockModel to get current prices
        # Assuming StockModel is accessible via PortfolioModel or passed separately
        # For now, let's assume it's accessible via self.model.api_client (if StockModel uses the same client)
        # A better approach might be to inject StockModel directly
        
        # Connect view signals to presenter slots
        self.view.buy_stock_requested.connect(self.buy_stock)
        self.view.sell_stock_requested.connect(self.sell_stock)
        self.view.refresh_requested.connect(self.update_portfolio)
        
    @Slot()
    def update_portfolio(self):
        """Update portfolio data using email/password and fetch current prices"""
        try:
            if not self.user_model.is_logged_in:
                self.portfolio_update_failed.emit("User not logged in")
                self.view.show_error("Please log in to view your portfolio")
                return
            
            # Get user credentials from ApiClient
            email = self.model.api_client.user_email
            password = self.model.api_client.user_password
            
            if not email or not password:
                 self.portfolio_update_failed.emit("User credentials not found")
                 self.view.show_error("Could not retrieve user credentials. Please log in again.")
                 return
                
            # 1. Get user holdings (symbol, quantity)
            holdings_raw = self.model.get_user_holdings(email, password)
            
            if not isinstance(holdings_raw, list):
                self.portfolio_update_failed.emit("Invalid holdings data received from API.")
                self.view.show_error("Received invalid holdings data.")
                return

            enriched_holdings = []
            total_portfolio_value = 0.0

            # 2. Fetch current price for each holding
            for holding in holdings_raw:
                symbol = holding.get("stockSymbol")
                quantity = holding.get("quantity")
                
                if not symbol or quantity is None:
                    print(f"Warning: Skipping invalid holding data: {holding}")
                    continue

                try:
                    # Use the api_client (shared instance) to get current price
                    current_price_response = self.model.api_client.get_current_stock_data(symbol)
                    # Assuming the response is the price directly (e.g., 210.555)
                    current_price = float(current_price_response) 
                except Exception as price_error:
                    print(f"Warning: Could not fetch current price for {symbol}: {price_error}")
                    current_price = 0.0 # Default to 0 if price fetch fails

                # 3. Calculate total value for the holding
                total_value_item = quantity * current_price
                total_portfolio_value += total_value_item

                # Add enriched data to the list
                enriched_holdings.append({
                    "stockSymbol": symbol,
                    "quantity": quantity,
                    "avg_price": holding.get("avg_price", 0.0), # Keep avg_price if available, else 0
                    "current_price": current_price,
                    "total_value": total_value_item
                })

            # 4. Get user transactions (assuming structure is okay)
            transactions = self.model.get_user_transactions(email, password)
            
            # 5. Update view with enriched holdings and transactions
            self.view.update_portfolio(enriched_holdings, total_portfolio_value)
            self.view.update_transactions(transactions)
            
            self.portfolio_updated.emit()
            
        except Exception as e:
            error_message = str(e)
            self.portfolio_update_failed.emit(error_message)
            self.view.show_error(f"Failed to update portfolio: {error_message}")
    
    @Slot(str, float)
    def buy_stock(self, symbol: str, quantity: float):
        """Handle buy stock request using email and password"""
        try:
            if not self.user_model.is_logged_in:
                self.transaction_failed.emit("User not logged in")
                self.view.show_error("Please log in to buy stocks")
                return
            
            # Get user credentials from ApiClient
            email = self.model.api_client.user_email
            password = self.model.api_client.user_password
            
            if not email or not password:
                 self.transaction_failed.emit("User credentials not found")
                 self.view.show_error("Could not retrieve user credentials. Please log in again.")
                 return
                
            # Create transaction using email and password
            result = self.model.create_transaction_by_email(
                email,
                password,
                symbol,
                quantity,
                "BUY"
            )
            
            # Update portfolio after transaction
            self.update_portfolio()
            
            self.transaction_successful.emit()
            self.view.show_success(f"Successfully bought {quantity} shares of {symbol}")
            
        except Exception as e:
            error_message = str(e)
            self.transaction_failed.emit(error_message)
            self.view.show_error(f"Failed to buy stock: {error_message}")
    
    @Slot(str, float)
    def sell_stock(self, symbol: str, quantity: float):
        """Handle sell stock request using email and password"""
        try:
            if not self.user_model.is_logged_in:
                self.transaction_failed.emit("User not logged in")
                self.view.show_error("Please log in to sell stocks")
                return
                
            # Get user credentials from ApiClient
            email = self.model.api_client.user_email
            password = self.model.api_client.user_password
            
            if not email or not password:
                 self.transaction_failed.emit("User credentials not found")
                 self.view.show_error("Could not retrieve user credentials. Please log in again.")
                 return
                
            # Create transaction using email and password
            result = self.model.create_transaction_by_email(
                email,
                password,
                symbol,
                quantity,
                "SELL"
            )
            
            # Update portfolio after transaction
            self.update_portfolio()
            
            self.transaction_successful.emit()
            self.view.show_success(f"Successfully sold {quantity} shares of {symbol}")
            
        except Exception as e:
            error_message = str(e)
            self.transaction_failed.emit(error_message)
            self.view.show_error(f"Failed to sell stock: {error_message}")
