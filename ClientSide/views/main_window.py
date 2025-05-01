from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon, QFont

from views.login_view import LoginView
from views.stock_chart_view import StockChartView
from views.portfolio_view import PortfolioView
from views.ai_advisor_view import AIAdvisorView
from views.dashboard_view import DashboardView
from views.navigation_bar import NavigationBar
from models.user_model import UserModel
from models.stock_model import StockModel
from models.portfolio_model import PortfolioModel
from presenters.login_presenter import LoginPresenter
from presenters.stock_chart_presenter import StockChartPresenter
from presenters.portfolio_presenter import PortfolioPresenter
from presenters.ai_advisor_presenter import AIAdvisorPresenter
from presenters.dashboard_presenter import DashboardPresenter
from utils.api_client import ApiClient

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_client = ApiClient()
        self.setup_models()
        self.setup_ui()
        self.setup_presenters()
        
    def setup_models(self):
        """Initialize model classes"""
        self.user_model = UserModel(self.api_client)
        self.stock_model = StockModel(self.api_client)
        self.portfolio_model = PortfolioModel(self.api_client)
        
    def setup_ui(self):
        """Setup the user interface"""
        # Set window properties
        self.setWindowTitle("Stock Market Analysis")
        self.setMinimumSize(1024, 768)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.central_widget)
        
        # Create navigation bar
        self.navigation_bar = NavigationBar()
        self.navigation_bar.view_changed.connect(self.show_view)
        self.navigation_bar.logout_requested.connect(self.logout)
        
        # Add navigation bar to main layout
        self.main_layout.addWidget(self.navigation_bar)
        
        # Hide navigation bar initially (show after login)
        self.navigation_bar.setVisible(False)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget, 1)
        
        # Create views
        self.login_view = LoginView()
        self.dashboard_view = DashboardView()
        self.stock_chart_view = StockChartView()
        self.portfolio_view = PortfolioView()
        self.ai_advisor_view = AIAdvisorView()
        
        # Add views to stacked widget
        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.stock_chart_view)
        self.stacked_widget.addWidget(self.portfolio_view)
        self.stacked_widget.addWidget(self.ai_advisor_view)
        
        # Show login view initially
        self.stacked_widget.setCurrentWidget(self.login_view)
        
    def setup_presenters(self):
        """Initialize presenter classes"""
        self.login_presenter = LoginPresenter(self.login_view, self.user_model)
        self.dashboard_presenter = DashboardPresenter(self.dashboard_view, self.stock_model, self.portfolio_model)
        self.stock_chart_presenter = StockChartPresenter(self.stock_chart_view, self.stock_model)
        self.portfolio_presenter = PortfolioPresenter(self.portfolio_view, self.portfolio_model, self.user_model)
        self.ai_advisor_presenter = AIAdvisorPresenter(self.ai_advisor_view, self.stock_model)
        
        # Connect login presenter signals
        self.login_presenter.login_successful.connect(self.on_login_successful)
        
    @Slot()
    def on_login_successful(self):
        """Handle successful login"""
        # Show navigation bar
        self.navigation_bar.setVisible(True)
        
        # Switch to dashboard view
        self.stacked_widget.setCurrentWidget(self.dashboard_view)
        
    @Slot()
    def logout(self):
        """Handle logout request"""
        # Logout user
        self.user_model.logout()
        
        # Hide navigation bar
        self.navigation_bar.setVisible(False)
        
        # Switch to login view
        self.stacked_widget.setCurrentWidget(self.login_view)
        
        # Clear login fields
        self.login_view.clear_fields()
        
        # Show logout message
        QMessageBox.information(self, "Logout", "You have been logged out successfully.")
        
    def show_view(self, view_name):
        """Show a specific view"""
        if view_name == "login":
            self.stacked_widget.setCurrentWidget(self.login_view)
        elif view_name == "dashboard":
            self.stacked_widget.setCurrentWidget(self.dashboard_view)
            # Refresh dashboard data when showing the view
            self.dashboard_presenter.update_dashboard()
        elif view_name == "chart":
            self.stacked_widget.setCurrentWidget(self.stock_chart_view)
        elif view_name == "portfolio":
            self.stacked_widget.setCurrentWidget(self.portfolio_view)
            # Refresh portfolio data when showing the view
            self.portfolio_presenter.update_portfolio()
        elif view_name == "advisor":
            self.stacked_widget.setCurrentWidget(self.ai_advisor_view)
        else:
            raise ValueError(f"Unknown view: {view_name}")
