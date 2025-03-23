import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox, QRadioButton, QButtonGroup, QHBoxLayout, QCheckBox
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

        self.headers = QCheckBox("Dodaj nagłowki")
        self.headers.setVisible(False)
        self.headers.toggled.connect(self.toggle_headers_bold)

        self.headers_bold = QCheckBox("Nagłówki pogrubione")
        self.headers_bold.setVisible(False)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.headers)
        hbox3.addWidget(self.headers_bold)
        self.layout.addLayout(hbox3)

        # Wybór czcionki
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Calibri", "Verdana"])
        self.font_combo.setCurrentText("Arial")
        self.font_combo.setVisible(False)

        # Wybór rozmiaru czcionki
        self.size_combo = QComboBox()
        self.size_combo.addItems(["10", "11", "12", "14", "16", "18", "20"])
        self.size_combo.setCurrentText("12")
        self.size_combo.setVisible(False)

        hbox_font = QHBoxLayout()
        hbox_font.addWidget(self.font_combo)
        hbox_font.addSpacing(20)  # odstęp
        hbox_font.addWidget(self.size_combo)
        self.layout.addLayout(hbox_font)

        # Button for hiding/showing preview
        self.toggle_preview_button = QPushButton("Pokaż podgląd")
        self.toggle_preview_button.clicked.connect(self.toggle_preview)
        self.toggle_preview_button.setVisible(False)
        self.layout.addWidget(self.toggle_preview_button)

        # Table for preview (hide by default)
        self.table = QTableWidget()
        self.table.setVisible(False)
        self.layout.addWidget(self.table)

        self.type_label = QLabel("Konwertuj jako")
        self.radio_table = QRadioButton("Tabela")
        self.radio_spaces = QRadioButton("Ze spacjami")
        self.radio_list = QRadioButton("Lista")
        self.radio_page = QRadioButton("Lista ze stronami")
        self.radio_table.setChecked(True)

        self.group_format = QButtonGroup(self)
        self.group_format.addButton(self.radio_table)
        self.group_format.addButton(self.radio_spaces)
        self.group_format.addButton(self.radio_list)
        self.group_format.addButton(self.radio_page)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.type_label)
        hbox1.addWidget(self.radio_table)
        hbox1.addWidget(self.radio_spaces)
        hbox1.addWidget(self.radio_list)
        hbox1.addWidget(self.radio_page)

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
            self.headers.setVisible(True)
            self.font_combo.setVisible(True)
            self.size_combo.setVisible(True)

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
        font_size = self.size_combo.currentText()
        font = self.font_combo.currentText()
        if self.radio_table.isChecked():
            form = 1
        elif self.radio_spaces.isChecked():
            form = 2
        elif self.radio_list.isChecked():
            form = 3
        else:
            form = 4
        if save_path:
            selected_sheet = self.sheet_selector.currentText()
            df = self.sheets[selected_sheet]
            df.to_excel("temp.xlsx", index=False)  # temp file with selected sheet

            convert_xlsx_to_docx("temp.xlsx", save_path, self.radio_pdf.isChecked(), self.headers.isChecked(), self.headers_bold.isChecked(), font_size, font, form)
            self.status_label.setText("Conversion successful!")

    def toggle_headers_bold(self):
        self.headers_bold.setVisible(True)
