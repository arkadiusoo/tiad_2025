import sys

from PyQt6.QtWidgets import QApplication

from Assignment_2.gui.main_window import MainWindow



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
