import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget
from converter import convert_xlsx_to_docx


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XLSX to DOCX Converter")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("Wybierz plik XLSX do konwersji:")
        self.layout.addWidget(self.label)

        self.button_select = QPushButton("Wybierz plik")
        self.button_select.clicked.connect(self.select_file)
        self.layout.addWidget(self.button_select)

        self.button_convert = QPushButton("Konwertuj do DOCX")
        self.button_convert.clicked.connect(self.convert_file)
        self.layout.addWidget(self.button_convert)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.xlsx_file = ""

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik XLSX", "", "Excel Files (*.xlsx)")
        if file_path:
            self.xlsx_file = file_path
            self.label.setText(f"Wybrano: {file_path}")

    def convert_file(self):
        if not self.xlsx_file:
            self.status_label.setText("Najpierw wybierz plik XLSX!")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Zapisz jako", "", "Word Files (*.docx)")
        if save_path:
            convert_xlsx_to_docx(self.xlsx_file, save_path)
            self.status_label.setText("Konwersja zakończona sukcesem!")
