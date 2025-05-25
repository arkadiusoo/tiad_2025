import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QLabel, QTextEdit, QFileDialog, QMessageBox,
    QHBoxLayout, QSizePolicy
)
from Assignment_2.audio import recorder
from Assignment_2.nlp import extractor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filtr przepisów głosowych")
        self.setMinimumSize(700, 500)

        self.locale = "pl-PL"

        # Przyciski
        self.button_record = QPushButton("Nagraj z mikrofonu")
        self.button_record.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.button_record.clicked.connect(self.handle_record)

        self.button_load = QPushButton("Wczytaj plik audio")
        self.button_load.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.button_load.clicked.connect(self.handle_load)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_record)
        button_layout.addWidget(self.button_load)

        # Składniki
        self.ingredients_label = QLabel("Wykryte składniki:")
        self.ingredients_text = QTextEdit()
        self.ingredients_text.setReadOnly(True)
        self.ingredients_text.setFixedHeight(100)

        # Przepisy
        self.recipes_label = QLabel("Dopasowane przepisy:")
        self.recipes_text = QTextEdit()
        self.recipes_text.setReadOnly(True)
        self.recipes_text.setFixedHeight(200)

        # Układ główny
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
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

            self.ingredients_text.setPlainText(", ".join(ingredients) if ingredients else "(brak)")
            if matches:
                results = "\n".join(
                    f"- {r['name']} ({', '.join(r['ingredients'])})"
                    for r in matches
                )
            else:
                results = "Nie znaleziono pasujących przepisów."
            self.recipes_text.setPlainText(results)
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))

    def handle_record(self):
        from Assignment_2.audio.recorder import MicrophoneRecorderDialog
        dialog = MicrophoneRecorderDialog(self)
        dialog.recording_finished.connect(self.process_audio_file)
        dialog.exec()

    def handle_load(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik audio", "", "Pliki audio (*.wav *.mp3 *.m4a)"
        )
        if file_path:
            self.process_audio_file(file_path)
