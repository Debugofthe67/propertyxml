from PySide6.QtWidgets import QTabWidget
from src.ui.dual_editor import DualEditor

class TabManager(QTabWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab_at)
        self.setStyleSheet("""
            QTabWidget::pane { border-top: 1px solid #2d2d2d; background: #181818; }
            QTabBar::tab {
                background: #1e1e1e; color: #999999; padding: 6px 14px;
                border-top-left-radius: 4px; border-top-right-radius: 4px;
                margin-right: 2px; border: 1px solid #2d2d2d; border-bottom: none;
            }
            QTabBar::tab:selected { background: #181818; color: #ffffff; font-weight: 600; }
        """)

    def add_plist_tab(self, title, file_path=None, data=None, dual_view_enabled=True):
        editor = DualEditor(file_path=file_path, data=data, dual_view_enabled=dual_view_enabled)
        index = self.addTab(editor, title)
        self.setCurrentIndex(index)
        return editor

    def close_tab_at(self, index):
        if self.main_window:
            self.main_window.close_tab(index)
        else:
            self.removeTab(index)
