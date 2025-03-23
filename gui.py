import json
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox, QRadioButton,
    QButtonGroup, QHBoxLayout, QCheckBox, QLineEdit, QMessageBox
)
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve

from converter import convert_xlsx_to_docx

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter pliku XLSX do Worda/PDF")
        self.resize(600, 450)
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        self.layout = QVBoxLayout()

        # Start screen - only label and button
        self.label = QLabel("Wybierz plik XLSX:")
        self.layout.addWidget(self.label)

        self.button_select = QPushButton("Wybierz plik")
        self.button_select.clicked.connect(self.select_file)
        self.layout.addWidget(self.button_select)

        # UI section appears after file selection
        self.init_secondary_ui()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.xlsx_file = ""
        self.sheets = {}

    def init_secondary_ui(self):
        self.sheet_selector = QComboBox()
        self.sheet_selector.currentTextChanged.connect(self.load_selected_sheet)
        self.sheet_selector.setVisible(False)
        self.layout.addWidget(self.sheet_selector)

        self.toggle_preview_button = QPushButton("Pokaż podgląd arukasz")
        self.toggle_preview_button.clicked.connect(self.toggle_preview)
        self.toggle_preview_button.setVisible(False)
        self.layout.addWidget(self.toggle_preview_button)

        self.table = QTableWidget()
        self.table.setVisible(False)
        self.layout.addWidget(self.table)

        self.title_label = QLabel("Tytuł dokumentu:")
        self.title_label.setVisible(False)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Wprowadź tytuł dokumentu (domyślnie zostanie dodana nazwa pliku XLSX)")
        self.title_input.setVisible(False)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_input)

        self.headers = QCheckBox("Dodaj nagłówki")
        self.headers.setVisible(False)

        self.headers_bold = QCheckBox("Nagłówki pogrubione")
        self.headers_bold.setVisible(False)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.headers)
        hbox3.addWidget(self.headers_bold)
        self.layout.addLayout(hbox3)

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Calibri", "Verdana"])
        self.font_combo.setCurrentText("Arial")
        self.font_combo.setVisible(False)

        self.size_combo = QComboBox()
        self.size_combo.addItems(["10", "11", "12", "14", "16", "18", "20"])
        self.size_combo.setCurrentText("12")
        self.size_combo.setVisible(False)

        hbox_font = QHBoxLayout()
        hbox_font.addWidget(self.font_combo)
        hbox_font.addSpacing(20)
        hbox_font.addWidget(self.size_combo)
        self.layout.addLayout(hbox_font)



        self.type_label = QLabel("Konwertuj jako")
        self.type_label.setVisible(False)

        self.radio_table = QRadioButton("Tabela")
        self.radio_spaces = QRadioButton("Ze spacjami")
        self.radio_list = QRadioButton("Lista")
        self.radio_page = QRadioButton("Lista ze stronami")
        self.radio_table.setChecked(True)

        for rb in [self.radio_table, self.radio_spaces, self.radio_list, self.radio_page]:
            rb.setVisible(False)

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
        self.layout.addLayout(hbox1)

        self.radio_docx = QRadioButton("Konwertuj do DOCX")
        self.radio_pdf = QRadioButton("Konwertuj do PDF")


        self.radio_docx.setChecked(True)

        self.radio_docx.setVisible(False)
        self.radio_pdf.setVisible(False)

        self.group_output = QButtonGroup(self)
        self.group_output.addButton(self.radio_docx)
        self.group_output.addButton(self.radio_pdf)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.radio_docx)
        hbox2.addWidget(self.radio_pdf)
        self.layout.addLayout(hbox2)

        self.button_convert = QPushButton("Konwertuj")
        self.button_convert.clicked.connect(self.convert_file)
        self.button_convert.setVisible(False)
        self.layout.addWidget(self.button_convert)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)
        self.status_label.setWordWrap(True)

        # visibility manage list
        self.secondary_widgets = [
            self.sheet_selector, self.headers, self.headers_bold,
            self.font_combo, self.size_combo, self.toggle_preview_button,
            self.button_convert, self.type_label, self.radio_table, self.radio_spaces,
            self.radio_list, self.radio_page, self.radio_docx, self.radio_pdf, self.title_label, self.title_input,
            self.headers_bold
        ]
        self.load_settings()

    def show_secondary_ui(self):
        for widget in self.secondary_widgets:
            widget.setVisible(True)
        self.radio_pdf.toggled.connect(self.warn_pdf)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik XLSX", "", "Excel Files (*.xlsx)")
        if file_path:
            self.xlsx_file = file_path
            self.original_file_name = file_path.split("/")[-1]
            self.label.setText(f"Wybrany plik: {self.original_file_name}")

            self.sheets = pd.read_excel(self.xlsx_file, sheet_name=None)
            self.sheet_selector.clear()
            self.sheet_selector.addItems(self.sheets.keys())
            self.show_secondary_ui()

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
            self.toggle_preview_button.setText("Pokaż podgląd")
            self.animate_resize(600, 450)
        else:
            self.table.setVisible(True)
            self.toggle_preview_button.setText("Ukryj podgląd arkusza")
            self.animate_resize(800, 600)

    def convert_file(self):
        if not self.xlsx_file:
            self.status_label.setText("Wybierz najpierw plik XLSX!")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Zapisz jako", "", "Word Files (*.docx)")
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
        self.warn_pdf()
        if save_path:
            selected_sheet = self.sheet_selector.currentText()
            df = self.sheets[selected_sheet]
            df.to_excel("temp.xlsx", index=False)

            convert_xlsx_to_docx("temp.xlsx", save_path, self.radio_pdf.isChecked(), self.headers.isChecked(),
                                 self.headers_bold.isChecked(), font_size, font,
                                 form, self.title_input.text() or self.original_file_name)
            self.status_label.setText("Konwersja przebiegła pomyślnie! Plik zapisano w lokalizacji:\n{}".format(save_path))

    def animate_resize(self, target_width, target_height):
        start_geometry = self.geometry()
        end_geometry = QRect(
            start_geometry.x(),
            start_geometry.y(),
            target_width,
            target_height
        )
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(end_geometry)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()


    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                data = json.load(f)
                self.title_input.setText(data.get("title", ""))
                self.font_combo.setCurrentText(data.get("font", "Arial"))
                self.size_combo.setCurrentText(data.get("font_size", "12"))
                self.headers.setChecked(data.get("headers", False))
                self.headers_bold.setChecked(data.get("headers_bold", False))
                format_value = data.get("form", 1)
                [self.radio_table, self.radio_spaces, self.radio_list, self.radio_page][format_value - 1].setChecked(
                    True)
                (self.radio_pdf if data.get("pdf", False) else self.radio_docx).setChecked(True)

    def save_settings(self):
        data = {
            "title": self.title_input.text(),
            "font": self.font_combo.currentText(),
            "font_size": self.size_combo.currentText(),
            "headers": self.headers.isChecked(),
            "headers_bold": self.headers_bold.isChecked(),
            "form": [self.radio_table, self.radio_spaces, self.radio_list, self.radio_page].index(
                self.group_format.checkedButton()) + 1,
            "pdf": self.radio_pdf.isChecked()
        }
        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def warn_pdf(self):
        if self.radio_pdf.isChecked():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Ograniczenie PDF")
            msg.setText(
                "Eksport do PDF nie jest wspierany na systemie Linux.\n\n"
                "Funkcja działa tylko na systemach Windows i macOS,\n"
                "i wymaga zainstalowanego programu Microsoft Word."
            )
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
