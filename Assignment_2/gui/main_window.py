import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QLabel, QFileDialog, QMessageBox,
    QScrollArea, QHBoxLayout, QFrame, QSizePolicy, QCheckBox
)
from Assignment_2.audio import recorder, translator
from Assignment_2.audio.translator import translate_words
from Assignment_2.nlp import extractor
from langdetect import detect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filtr przepisów głosowych")
        self.setMinimumSize(700, 500)
        self.locale = "pl-PL"

        self.last_ingredients = []
        self.last_recipes = []
        self.all_words = []

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

        # Checkbox
        self.checkbox_strict = QCheckBox("Tylko przepisy na które masz składniki")
        self.checkbox_strict.setChecked(False)
        self.checkbox_strict.stateChanged.connect(self.on_checkbox_changed)

        #Wykryte słowa
        self.words_label = QLabel("Wykryte słowa:")
        self.words_area = QScrollArea()
        self.words_container = QWidget()
        self.words_layout = QVBoxLayout()
        self.words_container.setLayout(self.words_layout)
        self.words_area.setWidgetResizable(True)
        self.words_area.setWidget(self.words_container)
        # Składniki
        self.ingredients_label = QLabel("Wykryte składniki:")
        self.ingredients_area = QScrollArea()
        self.ingredients_container = QWidget()
        self.ingredients_layout = QVBoxLayout()
        self.ingredients_container.setLayout(self.ingredients_layout)
        self.ingredients_area.setWidgetResizable(True)
        self.ingredients_area.setWidget(self.ingredients_container)

        # Przepisy
        self.recipes_label = QLabel("Dopasowane przepisy:")
        self.recipes_area = QScrollArea()
        self.recipes_container = QWidget()
        self.recipes_layout = QVBoxLayout()
        self.recipes_container.setLayout(self.recipes_layout)
        self.recipes_area.setWidgetResizable(True)
        self.recipes_area.setWidget(self.recipes_container)

        # Layout główny
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.words_label)
        layout.addWidget(self.words_area)
        layout.addWidget(self.ingredients_label)
        layout.addWidget(self.ingredients_area)
        layout.addWidget(self.checkbox_strict)
        layout.addWidget(self.recipes_label)
        layout.addWidget(self.recipes_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def process_audio_file(self, file_path):
        try:
            text = recorder.recognize_audio(file_path, self.locale)
            self.all_words = text
            print(self.all_words)
            detected_lang = detect(text)
            print(detected_lang)

            self.last_recipes = extractor.load_recipes()
            known = extractor.known_ingredients_set(self.last_recipes)

            words = text.lower().split()
            print(words)
            translated_words = translate_words(words, dest='en')
            print(translated_words)


            self.last_ingredients = [w for w in translated_words if w in known]
            print(self.last_ingredients)

            matches = extractor.filter_recipes(
                self.last_recipes,
                self.last_ingredients,
                self.checkbox_strict.isChecked()
            )

            self.clear_layout(self.ingredients_layout)
            for ing in self.last_ingredients:
                self.ingredients_layout.addWidget(self.create_ingredient_tile(ing))

            self.clear_layout(self.recipes_layout)
            for recipe in matches:
                self.recipes_layout.addWidget(self.create_recipe_tile(recipe, self.last_ingredients))
            self.clear_layout((self.words_layout))
            for word in self.all_words.split():
                self.words_layout.addWidget(self.create_ingredient_tile(word))
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))

    def on_checkbox_changed(self, _):
        if not self.last_recipes or not self.last_ingredients:
            return

        matches = extractor.filter_recipes(
            self.last_recipes,
            self.last_ingredients,
            self.checkbox_strict.isChecked()
        )

        self.clear_layout(self.recipes_layout)
        for recipe in matches:
            self.recipes_layout.addWidget(self.create_recipe_tile(recipe, self.last_ingredients))

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

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_ingredient_tile(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            background-color: #2b2b2b;
            color: white;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 14px;
        """)
        return label

    def create_recipe_tile(self, recipe, detected_ingredients):
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #333;
            color: white;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 8px;
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        name = QLabel(f"<b>{recipe['name']}</b>")
        name.setStyleSheet("color: white; font-size: 15px;")
        layout.addWidget(name)

        highlighted = []
        for ing in recipe['ingredients_en']:
            if ing in detected_ingredients:
                highlighted.append(f"<span style='color: lightgreen'>{ing}</span>")
            else:
                highlighted.append(f"<span style='color: red'>{ing}</span>")
        ingredients = QLabel(", ".join(highlighted))
        ingredients.setStyleSheet("font-size: 13px;")
        ingredients.setTextFormat(Qt.TextFormat.RichText)

        layout.addWidget(ingredients)
        frame.setLayout(layout)
        return frame