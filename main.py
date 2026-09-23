import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import PropertyXMLWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PropertyXMLWindow()
    window.show()
    sys.exit(app.exec())
