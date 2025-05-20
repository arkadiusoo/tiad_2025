from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Recipe Filter")
        self.setMinimumSize(600, 400)

        # main widgets
        self.audio_button = QPushButton("Load or Record Audio")
        self.audio_button.clicked.connect(self.load_audio)

        self.ingredient_label = QLabel("Detected Ingredients:")
        self.ingredient_list = QListWidget()

        self.filter_button = QPushButton("Filter Recipes")
        self.filter_button.clicked.connect(self.filter_recipes)

        self.recipe_label = QLabel("Filtered Recipes:")
        self.recipe_list = QListWidget()

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.audio_button)
        layout.addWidget(self.ingredient_label)
        layout.addWidget(self.ingredient_list)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.recipe_label)
        layout.addWidget(self.recipe_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_audio(self):
        # goal: recording or loading an audio file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "", "Audio Files (*.wav *.mp3)"
        )
        if file_path:
            QMessageBox.information(self, "Audio Loaded", f"Loaded: {file_path}")
            # TODO: Call function and update the list of components
            self.ingredient_list.clear()
            self.ingredient_list.addItem("tomato")
            self.ingredient_list.addItem("onion")
            self.ingredient_list.addItem("salt")

    def filter_recipes(self):
        # TODO: Search the recipe database by ingredients
        self.recipe_list.clear()
        self.recipe_list.addItem("Tomato Soup")
        self.recipe_list.addItem("Grilled Vegetables")