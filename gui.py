import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox, QRadioButton, QButtonGroup, QHBoxLayout
)
from converter import convert_xlsx_to_docx

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XLSX to DOCX/PDF Converter")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # File detection label
        self.label = QLabel("Choose XLSX file to convert:")
        self.layout.addWidget(self.label)

        # File selection button
        self.button_select = QPushButton("Select file")
        self.button_select.clicked.connect(self.select_file)
        self.layout.addWidget(self.button_select)

        # ComboBox for sheet selection (hide by default)
        self.sheet_selector = QComboBox()
        self.sheet_selector.currentTextChanged.connect(self.load_selected_sheet)
        self.sheet_selector.setVisible(False)
        self.layout.addWidget(self.sheet_selector)

        # Button for hiding/showing preview
        self.toggle_preview_button = QPushButton("Pokaż podgląd")
        self.toggle_preview_button.clicked.connect(self.toggle_preview)
        self.toggle_preview_button.setVisible(False)
        self.layout.addWidget(self.toggle_preview_button)

        # Table for preview (hide by default)
        self.table = QTableWidget()
        self.table.setVisible(False)
        self.layout.addWidget(self.table)

        self.radio_table = QRadioButton("Konwertuj do tabeli")
        self.radio_spaces = QRadioButton("Konwertuj ze spacjami")
        self.radio_table.setChecked(True)

        self.group_format = QButtonGroup(self)
        self.group_format.addButton(self.radio_table)
        self.group_format.addButton(self.radio_spaces)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.radio_table)
        hbox1.addWidget(self.radio_spaces)

        # Grupa druga (DOCX lub PDF)
        self.radio_docx = QRadioButton("Konwertuj do DOCX")
        self.radio_pdf = QRadioButton("Konwertuj do PDF")
        self.radio_docx.setChecked(True)

        self.group_output = QButtonGroup(self)
        self.group_output.addButton(self.radio_docx)
        self.group_output.addButton(self.radio_pdf)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.radio_docx)
        hbox2.addWidget(self.radio_pdf)

        # Dodanie elementów do głównego layoutu
        self.layout.addLayout(hbox1)
        self.layout.addLayout(hbox2)
        # Conver button
        self.button_convert = QPushButton("Konwertuj")
        self.button_convert.clicked.connect(self.convert_file)
        self.button_convert.setVisible(False)
        self.layout.addWidget(self.button_convert)

        # Status label
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # Layout container
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.xlsx_file = ""
        self.sheets = {}

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose XLSX file", "", "Excel Files (*.xlsx)")
        if file_path:
            self.xlsx_file = file_path
            self.label.setText(f"Selected: {file_path}")

            # loading sheets
            self.sheets = pd.read_excel(self.xlsx_file, sheet_name=None)
            self.sheet_selector.clear()
            self.sheet_selector.addItems(self.sheets.keys())

            # Visibility toggling
            self.sheet_selector.setVisible(True)
            self.button_convert.setVisible(True)
            self.toggle_preview_button.setVisible(True)

            # First sheet by default
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

    def toggle_preview(self):
        if self.table.isVisible():
            self.table.setVisible(False)
            self.toggle_preview_button.setText("Show preview")
        else:
            self.table.setVisible(True)
            self.toggle_preview_button.setText("Hide preview")

    def convert_file(self):
        if not self.xlsx_file:
            self.status_label.setText("Choose XLSX file first!")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save as", "", "Word Files (*.docx)")
        if save_path:
            selected_sheet = self.sheet_selector.currentText()
            df = self.sheets[selected_sheet]
            df.to_excel("temp.xlsx", index=False)  # temp file with selected sheet

            convert_xlsx_to_docx("temp.xlsx", save_path, self.radio_table.isChecked(), self.radio_pdf.isChecked())
            self.status_label.setText("Conversion successful!")
