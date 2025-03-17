import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox
)
from converter import convert_xlsx_to_docx

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XLSX to DOCX Converter")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Etykieta wyboru pliku
        self.label = QLabel("Wybierz plik XLSX do konwersji:")
        self.layout.addWidget(self.label)

        # Przycisk wyboru pliku
        self.button_select = QPushButton("Wybierz plik")
        self.button_select.clicked.connect(self.select_file)
        self.layout.addWidget(self.button_select)


        if self.path
        # ComboBox do wyboru arkusza
        self.sheet_selector = QComboBox()
        self.sheet_selector.currentTextChanged.connect(self.load_selected_sheet)
        self.layout.addWidget(self.sheet_selector)

        # Tabela do podglądu pliku
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Przycisk konwersji
        self.button_convert = QPushButton("Konwertuj do DOCX")
        self.button_convert.clicked.connect(self.convert_file)
        self.layout.addWidget(self.button_convert)

        # Status operacji
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # Kontener na layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.xlsx_file = ""
        self.sheets = {}

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik XLSX", "", "Excel Files (*.xlsx)")
        if file_path:
            self.xlsx_file = file_path
            self.label.setText(f"Wybrano: {file_path}")

            # Wczytanie arkuszy
            self.sheets = pd.read_excel(self.xlsx_file, sheet_name=None)
            self.sheet_selector.clear()
            self.sheet_selector.addItems(self.sheets.keys())

            # Domyślnie wczytaj pierwszy arkusz
            first_sheet = self.sheet_selector.currentText()
            if first_sheet:
                self.load_sheet(first_sheet)

    def load_selected_sheet(self):
        sheet_name = self.sheet_selector.currentText()
        if sheet_name:
            self.load_sheet(sheet_name)

    def load_sheet(self, sheet_name):
        df = self.sheets[sheet_name]
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def convert_file(self):
        if not self.xlsx_file:
            self.status_label.setText("Najpierw wybierz plik XLSX!")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Zapisz jako", "", "Word Files (*.docx)")
        if save_path:
            selected_sheet = self.sheet_selector.currentText()
            df = self.sheets[selected_sheet]
            df.to_excel("temp.xlsx", index=False)  # Tymczasowy plik z wybranym arkuszem

            convert_xlsx_to_docx("temp.xlsx", save_path)
            self.status_label.setText("Konwersja zakończona sukcesem!")

