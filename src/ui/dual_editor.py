import plistlib
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTreeWidget, 
    QTreeWidgetItem, QTextEdit, QHeaderView, QSplitter
)
from PySide6.QtCore import Qt

class DualEditor(QWidget):
    def __init__(self, file_path=None, data=None, dual_view_enabled=True):
        super().__init__()
        self.file_path = file_path
        self.data = data if data is not None else {"RootKey": "RootValue"}
        self.is_dirty = False
        self.dual_view_enabled = dual_view_enabled
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tree View with Grid Lines & Alternating Rows
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Key", "Type", "Value"])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setRootIsDecorated(True)
        self.tree_widget.setUniformRowHeights(True)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: #181818;
                color: #e0e0e0;
                alternate-background-color: #1c1c1c;
                gridline-color: #2a2a2a;
                border: none;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #222222;
                color: #cccccc;
                padding: 5px;
                border: none;
                border-right: 1px solid #2d2d2d;
                border-bottom: 1px solid #2d2d2d;
                font-weight: 600;
            }
            QTreeWidget::item {
                padding: 4px;
                border-bottom: 1px solid #222222;
            }
            QTreeWidget::item:selected {
                background-color: #264f78;
                color: #ffffff;
            }
        """)
        
        header = self.tree_widget.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.populate_tree(self.data, self.tree_widget.invisibleRootItem())
        
        # Source Text View
        self.source_edit = QTextEdit()
        self.source_edit.setStyleSheet("""
            QTextEdit {
                background-color: #181818;
                color: #d4d4d4;
                font-family: SF Mono, Consolas, Monaco, monospace;
                font-size: 13px;
                border: none;
                padding: 8px;
            }
        """)
        self.update_source_view()
        self.source_edit.textChanged.connect(self.mark_dirty)
        
        if self.dual_view_enabled:
            # Tabbed ViewSwitcher (Tree View vs Source View tabs at the bottom)
            self.view_tabs = QTabWidget()
            self.view_tabs.setTabPosition(QTabWidget.South)
            self.view_tabs.setStyleSheet("""
                QTabWidget::pane { border: none; background: #181818; }
                QTabBar::tab {
                    background: #222222; color: #a0a0a0; padding: 6px 16px;
                    border-top: 1px solid #2d2d2d; border-right: 1px solid #2d2d2d;
                }
                QTabBar::tab:selected { background: #181818; color: #ffffff; font-weight: bold; }
            """)
            self.view_tabs.addTab(self.tree_widget, "Tree View")
            self.view_tabs.addTab(self.source_edit, "Source View")
            layout.addWidget(self.view_tabs)
        else:
            # Only display Tree View if dual-view setting is disabled
            layout.addWidget(self.tree_widget)

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

    def update_source_view(self):
        try:
            xml_data = plistlib.dumps(self.data, fmt=plistlib.FMT_XML).decode('utf-8')
            self.source_edit.setText(xml_data)
        except Exception:
            self.source_edit.setText(str(self.data))

    def mark_dirty(self):
        self.is_dirty = True
