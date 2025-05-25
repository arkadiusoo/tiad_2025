import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QLabel, QTextEdit, QFileDialog, QMessageBox
)
from Assignment_2.audio import recorder
from Assignment_2.nlp import extractor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Recipe Filter")
        self.setMinimumSize(600, 400)

        self.locale = "pl-PL"

        self.button_record = QPushButton("Record Audio from Microphone")
        self.button_record.clicked.connect(self.handle_record)

        self.button_load = QPushButton("Load Audio File")
        self.button_load.clicked.connect(self.handle_load)

        self.ingredients_label = QLabel("Detected Ingredients:")
        self.ingredients_text = QTextEdit()
        self.ingredients_text.setReadOnly(True)

        self.recipes_label = QLabel("Matching Recipes:")
        self.recipes_text = QTextEdit()
        self.recipes_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.button_record)
        layout.addWidget(self.button_load)
        layout.addWidget(self.ingredients_label)
        layout.addWidget(self.ingredients_text)
        layout.addWidget(self.recipes_label)
        layout.addWidget(self.recipes_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def process_audio_file(self, file_path):
        try:
            text = recorder.recognize_audio(file_path, self.locale)
            recipes = extractor.load_recipes()
            known = extractor.known_ingredients_set(recipes)
            ingredients = extractor.extract_ingredients(text, known)
            matches = extractor.filter_recipes(recipes, ingredients)

            self.ingredients_text.setPlainText(", ".join(ingredients) if ingredients else "(none)")
            if matches:
                results = "\n".join(
                    f"- {r['name']} ({', '.join(r['ingredients'])})"
                    for r in matches
                )
            else:
                results = "No matching recipes found."
            self.recipes_text.setPlainText(results)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def handle_record(self):
        file_path = recorder.record_microphone()
        self.process_audio_file(file_path)

    def handle_load(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "", "Audio Files (*.wav *.mp3, *.m4a)"
        )
        if file_path:
            self.process_audio_file(file_path)