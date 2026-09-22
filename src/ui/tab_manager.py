from PySide6.QtWidgets import QTabWidget
from src.ui.dual_editor import DualEditor

class TabManager(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_plist_tab(self, title, data, raw_text=""):
        editor = DualEditor(data, raw_text)
        index = self.addTab(editor, title)
        self.setCurrentIndex(index)

    def close_tab(self, index):
        self.removeTab(index)
