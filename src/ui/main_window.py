import plistlib
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from src.core.plist_handler import PlistHandler
from src.ui.titlebar import TitleBar
from src.ui.tab_manager import TabManager

class PropertyXMLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PropertyXML")
        self.resize(1100, 750)
        
        # Rounded window corners setup
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        
        container = QWidget(self)
        container.setObjectName("MainWindowContainer")
        container.setStyleSheet("""
            QWidget#MainWindowContainer {
                background-color: #181818;
                border: 1px solid #333333;
                border-radius: 10px;
            }
        """)
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(12, 8, 12, 8)
        toolbar_layout.setSpacing(8)
        
        btn_new = QPushButton("New")
        btn_open = QPushButton("Open...")
        btn_save = QPushButton("Save")
        btn_save_as = QPushButton("Save As...")
        btn_close = QPushButton("Close Tab")
        
        for btn in [btn_new, btn_open, btn_save, btn_save_as, btn_close]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #252525; color: #d1d1d1; border: 1px solid #333333;
                    padding: 5px 14px; border-radius: 5px; font-size: 12px; font-weight: 500;
                }
                QPushButton:hover { background-color: #2d2d2d; border-color: #444444; color: #ffffff; }
                QPushButton:pressed { background-color: #1f1f1f; }
            """)
            
        btn_new.clicked.connect(self.new_file)
        btn_open.clicked.connect(self.open_file)
        btn_save.clicked.connect(self.save_file)
        btn_save_as.clicked.connect(self.save_file_as)
        btn_close.clicked.connect(lambda: self.close_tab(self.tab_manager.currentIndex()))
        
        toolbar_layout.addWidget(btn_new)
        toolbar_layout.addWidget(btn_open)
        toolbar_layout.addWidget(btn_save)
        toolbar_layout.addWidget(btn_save_as)
        toolbar_layout.addWidget(btn_close)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)
        
        # Tab Manager
        self.tab_manager = TabManager(self)
        main_layout.addWidget(self.tab_manager)
        
        self.setCentralWidget(container)
        self.new_file()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.centralWidget().setGeometry(0, 0, self.width(), self.height())

    def new_file(self):
        self.tab_manager.add_plist_tab("Untitled.plist")

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Property List", "", "Plist Files (*.plist *.xml *.bplist);;All Files (*.*)"
        )
        if file_name:
            try:
                data = PlistHandler.load(file_name)
                short_name = Path(file_name).name
                self.tab_manager.add_plist_tab(short_name, file_path=file_name, data=data)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to parse plist file:\n{e}")

    def save_file(self):
        current_editor = self.tab_manager.currentWidget()
        if not current_editor:
            return
        if current_editor.file_path:
            try:
                text_content = current_editor.source_edit.toPlainText().encode('utf-8')
                parsed_data = plistlib.loads(text_content)
                PlistHandler.save(parsed_data, current_editor.file_path)
                current_editor.is_dirty = False
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        current_editor = self.tab_manager.currentWidget()
        if not current_editor:
            return
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Property List As", "", "Plist Files (*.plist *.xml);;All Files (*.*)"
        )
        if file_name:
            current_editor.file_path = file_name
            self.tab_manager.setTabText(self.tab_manager.currentIndex(), Path(file_name).name)
            self.save_file()

    def close_tab(self, index):
        if index < 0:
            return
        editor = self.tab_manager.widget(index)
        if editor.is_dirty:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "This file has unsaved changes. Do you want to discard them?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.tab_manager.setCurrentIndex(index)
                self.save_file()
                return
            elif reply == QMessageBox.Cancel:
                return
        self.tab_manager.removeTab(index)

    def close_current_tab_or_window(self):
        if self.tab_manager.count() > 0:
            self.close_tab(self.tab_manager.currentIndex())
        else:
            self.close()
