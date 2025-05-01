from PySide6.QtCore import QObject, Signal, Slot
from typing import Dict, Any

class AIAdvisorPresenter(QObject):
    """
    Presenter class for AI advisor view
    Handles the communication between AI advisor view and stock model
    """
    
    advice_received = Signal(str)
    advice_failed = Signal(str)
    
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        
        # Connect view signals to presenter slots
        self.view.advice_requested.connect(self.get_advice)
        self.view.history_advice_requested.connect(self.get_history_based_advice)
        
    @Slot(str)
    def get_advice(self, query: str):
        """Handle general advice request"""
        try:
            advice = self.model.get_ai_advice(query)
            
            # Display advice
            self.view.display_advice(advice)
            self.advice_received.emit(advice)
            
        except Exception as e:
            error_message = str(e)
            self.advice_failed.emit(error_message)
            self.view.show_error(f"Failed to get advice: {error_message}")
    
    @Slot(str)
    def get_history_based_advice(self, stock_symbol: str):
        """Handle stock history based advice request"""
        try:
            advice = self.model.get_history_based_advice(stock_symbol)
            
            # Display advice
            self.view.display_advice(advice)
            self.advice_received.emit(advice)
            
        except Exception as e:
            error_message = str(e)
            self.advice_failed.emit(error_message)
            self.view.show_error(f"Failed to get advice for {stock_symbol}: {error_message}")
