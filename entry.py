import sys
from PyQt6.QtWidgets import QApplication
from src import DZAutoClickerUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = DZAutoClickerUI()
    sys.exit(app.exec())
