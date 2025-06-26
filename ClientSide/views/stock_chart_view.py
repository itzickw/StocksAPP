from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont, QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis

class StockChartView(QWidget):
    """Stock chart view component for displaying stock price charts"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        controls_layout = QHBoxLayout()

        # Symbol selection
        symbol_box = QHBoxLayout()
        symbol_label = QLabel("Symbol:")
        self.symbol_combo = QComboBox()
        self.symbol_combo.setStyleSheet("QComboBox { border: 2px solid #0078d7; border-radius: 4px; }")
        self.symbol_combo.setEditable(True)
        self.symbol_combo.addItems(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"])
        self.symbol_combo.setMinimumWidth(100)
        symbol_box.addWidget(symbol_label)
        symbol_box.addWidget(self.symbol_combo)

        # Time range selection
        range_box = QHBoxLayout()
        range_label = QLabel("Time Range:")
        self.range_combo = QComboBox()
        self.range_combo.setStyleSheet("QComboBox { border: 2px solid #0078d7; border-radius: 4px; }")
        self.range_combo.addItems(["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "3 Years"])
        self.range_combo.setCurrentText("1 Month")
        self.range_combo.setMinimumWidth(100)
        range_box.addWidget(range_label)
        range_box.addWidget(self.range_combo)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setMinimumWidth(80)

        # Assemble control layout with spacing
        controls_layout.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        controls_layout.addLayout(symbol_box)
        controls_layout.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        controls_layout.addLayout(range_box)
        controls_layout.addSpacerItem(QSpacerItem(500, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        controls_layout.addWidget(self.refresh_button)

        main_layout.addLayout(controls_layout)

        self.chart = QChart()
        self.chart.setTitle("Stock Price Chart")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        main_layout.addWidget(self.chart_view)

    def update_line_chart(self, data):
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        if not data:
            self.chart.setTitle("No data available")
            return

        self.chart.setTitle(f"{self.symbol_combo.currentText()} Price Chart")

        series = QLineSeries()
        series.setName(f"{self.symbol_combo.currentText()} Price")

        min_y = float("inf")
        max_y = float("-inf")
        min_x_dt = None
        max_x_dt = None

        for point in data:
            date_str = point["date"]
            price = point["price"]
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

        axis_x = QDateTimeAxis()
        axis_x.setFormat("MMM dd yyyy")
        axis_x.setTitleText("Date")
        if min_x_dt and max_x_dt:
            axis_x.setMin(min_x_dt)
            axis_x.setMax(max_x_dt)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("$%.2f")
        axis_y.setTitleText("Price ($)")

        if min_y != float("inf") and max_y != float("-inf"):
            padding_y = (max_y - min_y) * 0.1 if max_y > min_y else 1.0
            axis_y.setMin(min_y - padding_y)
            axis_y.setMax(max_y + padding_y)
        else:
            axis_y.setMin(0)
            axis_y.setMax(100)

        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

    def clear_chart(self):
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
        self.chart.setTitle("No data available")

    def show_error(self, message):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Chart Error", message)
