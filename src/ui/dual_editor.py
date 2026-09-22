from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTreeWidget, QTreeWidgetItem, QTextEdit
import plistlib

class DualEditor(QWidget):
    def __init__(self, data=None, raw_text=""):
        super().__init__()
        self.data = data
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Inner view switcher (Tree View vs Source View)
        self.view_tabs = QTabWidget()
        self.view_tabs.setTabPosition(QTabWidget.South)
        
        # Tree View Component
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Key", "Type", "Value"])
        self.populate_tree(self.data, self.tree_widget.invisibleRootItem())
        
        # Source Text View Component
        self.source_edit = QTextEdit()
        if raw_text:
            self.source_edit.setText(raw_text)
        else:
            try:
                self.source_edit.setText(plistlib.dumps(data, fmt=plistlib.FMT_XML).decode('utf-8'))
            except Exception:
                self.source_edit.setText(str(data))
                
        self.view_tabs.addTab(self.tree_widget, "Tree View")
        self.view_tabs.addTab(self.source_edit, "Source View")
        
        layout.addWidget(self.view_tabs)

    def populate_tree(self, value, parent_item):
        if isinstance(value, dict):
            for k, v in value.items():
                item = QTreeWidgetItem([str(k), type(v).__name__, ""])
                parent_item.addChild(item)
                self.populate_tree(v, item)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                item = QTreeWidgetItem([f"[{i}]", type(v).__name__, ""])
                parent_item.addChild(item)
                self.populate_tree(v, item)
        else:
            parent_item.setText(2, str(value))
