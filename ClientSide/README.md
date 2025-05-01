# Stock Market Analysis Application

A desktop application built with PySide6 that connects to the Gateway API for stock market analysis and portfolio management.

## Features

- **User Authentication**: Secure login and registration using V2 endpoints
- **Dashboard**: Overview of market indices and portfolio performance with interactive charts
- **Stock Charts**: Visualize stock price history with line and candlestick charts
- **Portfolio Management**: Track your stock holdings and transactions with pie chart visualization
- **AI Advisor**: Get AI-powered investment advice and stock analysis

## Requirements

- Python 3.8+
- PySide6
- Requests

## Installation

1. Extract the zip file to a directory of your choice
2. Install the required packages:

```bash
pip install PySide6 requests
```

3. Configure the API endpoint in `utils/api_client.py` if needed (default is `http://localhost:9000`)

## Running the Application

From the application directory, run:

```bash
python main.py
```

## Architecture

The application follows the Model-View-Presenter (MVP) architecture:

- **Models**: Handle data and business logic, including API communication
- **Views**: Handle UI components and user interaction
- **Presenters**: Connect the Models and Views, handling the application logic

## Directory Structure

```
stock_app/
├── main.py                  # Application entry point
├── models/                  # Model classes
│   ├── stock_model.py       # Stock data model
│   ├── user_model.py        # User authentication model
│   └── portfolio_model.py   # Portfolio management model
├── views/                   # View classes
│   ├── login_view.py        # Login and registration view
│   ├── dashboard_view.py    # Dashboard overview view
│   ├── stock_chart_view.py  # Stock chart visualization view
│   ├── portfolio_view.py    # Portfolio management view
│   ├── ai_advisor_view.py   # AI advisor view
│   ├── navigation_bar.py    # Navigation component
│   └── main_window.py       # Main application window
├── presenters/              # Presenter classes
│   ├── login_presenter.py        # Login presenter
│   ├── dashboard_presenter.py    # Dashboard presenter
│   ├── stock_chart_presenter.py  # Stock chart presenter
│   ├── portfolio_presenter.py    # Portfolio presenter
│   └── ai_advisor_presenter.py   # AI advisor presenter
└── utils/                   # Utility classes
    └── api_client.py        # API client for Gateway API
```

## API Integration

The application connects to the Gateway API using the API client in `utils/api_client.py`. The client handles all API requests to the gateway server, including:

- User authentication (V2 endpoints only)
- Stock data retrieval
- Portfolio management
- AI advisor requests

## Visualization

The application uses QTCharts for data visualization, including:

- Line charts for stock price history
- Candlestick charts for OHLC data
- Pie charts for portfolio allocation
- Bar charts for market indices and top gainers/losers

## Notes

- The application uses only V2 endpoints for user-related functionality as requested
- All UI text and labels are in English
- The application is designed to be responsive and user-friendly
