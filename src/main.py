import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt
from src.ui.titlebar import TitleBar
from src.ui.tab_manager import TabManager
from src.core.plist_handler import PlistHandler

class PropertyXMLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PropertyXML")
        self.resize(1100, 750)
        
        # Frameless window configuration
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet("background-color: #121212; color: #ffffff;")
        
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom TitleBar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Toolbar actions (New, Open, Save, Close)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 6, 10, 6)
        
        btn_new = QPushButton("New")
        btn_open = QPushButton("Open...")
        btn_save = QPushButton("Save")
        
        for btn in [btn_new, btn_open, btn_save]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d; color: #fff; border: 1px solid #3d3d3d;
                    padding: 5px 12px; border-radius: 4px; font-size: 12px;
                }
                QPushButton:hover { background-color: #3d3d3d; }
            """)
            
        btn_new.clicked.connect(self.new_file)
        btn_open.clicked.connect(self.open_file)
        
        toolbar_layout.addWidget(btn_new)
        toolbar_layout.addWidget(btn_open)
        toolbar_layout.addWidget(btn_save)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)
        
        # Multi-File Tab Manager
        self.tab_manager = TabManager()
        main_layout.addWidget(self.tab_manager)
        
        self.setCentralWidget(central_widget)

    def new_file(self):
        empty_data = {"RootKey": "RootValue"}
        self.tab_manager.add_plist_tab("Untitled.plist", empty_data)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Property List", "", "Plist Files (*.plist *.xml *.bplist);;All Files (*.*)"
        )
        if file_name:
            try:
                data = PlistHandler.load(file_name)
                with open(file_name, "rb") as f:
                    raw = f.read().decode('utf-8', errors='ignore')
                
                short_name = file_name.split("/")[-1]
                self.tab_manager.add_plist_tab(short_name, data, raw)
            except Exception as e:
                print(f"Failed to parse plist: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PropertyXMLWindow()
    window.show()
    sys.exit(app.exec())
