from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, QPoint

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(38)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #d1d1d1;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
                font-size: 13px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid #2d2d2d;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(8)
        
        # macOS-style Traffic Lights (Top-Left)
        self.btn_close = self.create_traffic_light("#ff5f56", self.parent.close_current_tab_or_window)
        self.btn_min = self.create_traffic_light("#ffbd2e", self.parent.showMinimized)
        self.btn_max = self.create_traffic_light("#27c93f", self.toggle_maximize)
        
        layout.addWidget(self.btn_close)
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        
        layout.addSpacing(12)
        self.title_label = QLabel("PropertyXML")
        self.title_label.setStyleSheet("color: #888888; font-weight: 600; border: none;")
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        self.start_pos = QPoint()

    def create_traffic_light(self, color, callback):
        btn = QPushButton()
        btn.setFixedSize(12, 12)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{ opacity: 0.8; }}
        """)
        btn.clicked.connect(callback)
        return btn

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()
