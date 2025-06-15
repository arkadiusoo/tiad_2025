from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QFileDialog, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Assignment_3.utils import data_loader
from Assignment_3.models import model_loader
from Assignment_3.utils.metrics import evaluate_model

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐶🐱 Dogs vs Cats Classifier")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["ResNet50", "VGG16", "EfficientNetB0"])
        self.layout.addWidget(self.model_label)
        self.layout.addWidget(self.model_combo)

        self.split_label = QLabel("Train/Test Split (0.6, 0.7, 0.8):")
        self.split_input = QLineEdit("0.8")
        self.layout.addWidget(self.split_label)
        self.layout.addWidget(self.split_input)

        self.path_label = QLabel("Dataset Path:")
        self.path_input = QLineEdit("Assignment_3/data/dataset/training_set")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.path_input)
        self.layout.addWidget(self.browse_button)

        self.epochs_label = QLabel("Epochs:")
        self.epochs_input = QSpinBox()
        self.epochs_input.setRange(1, 100)
        self.epochs_input.setValue(1)
        self.layout.addWidget(self.epochs_label)
        self.layout.addWidget(self.epochs_input)

        self.start_button = QPushButton("Start Training")
        self.start_button.clicked.connect(self.run_training)
        self.layout.addWidget(self.start_button)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Dataset Folder")
        if folder:
            self.path_input.setText(folder)

    def run_training(self):
        model_name = self.model_combo.currentText()
        try:
            split = float(self.split_input.text())
            if split not in [0.6, 0.7, 0.8]:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Błąd", "Podział musi wynosić 0.6, 0.7 lub 0.8")
            return

        dataset_path = self.path_input.text()
        epochs = self.epochs_input.value()

        train_gen, val_gen = data_loader.get_data_generators(dataset_path, split_ratio=split)
        model = model_loader.get_model(model_name)
        model.fit(train_gen, validation_data=val_gen, epochs=epochs)

        acc = model.evaluate(val_gen, verbose=0)[1]
        QMessageBox.warning(self, "Results", f"Accuracy: {acc:.2%}")

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(model.history.history['accuracy'], label='Train Accuracy')
        ax.plot(model.history.history['val_accuracy'], label='Validation Accuracy')
        ax.legend()
        ax.set_title("Accuracy vs Epochs")
        self.canvas.draw()
