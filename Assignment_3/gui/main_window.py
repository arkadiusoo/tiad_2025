import numpy as np
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QFileDialog, QSpinBox, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QRect
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Assignment_3.utils import data_loader
from Assignment_3.models import model_loader
from Assignment_3.utils.metrics import evaluate_model

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐶🐱 Dogs vs Cats Classifier")

        self.resize(1200, 800)

        # Center on second screen if available
        width, height = 1200, 800
        screens = QGuiApplication.screens()
        target_screen = screens[1] if len(screens) > 1 else screens[0]
        screen_geometry: QRect = target_screen.geometry()
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.move(x, y)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create tabs for training and prediction
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Tab 1: Training
        self.train_tab = QWidget()
        self.train_layout = QVBoxLayout()
        self.train_tab.setLayout(self.train_layout)
        self.tabs.addTab(self.train_tab, "Train")

        # Tab 2: Prediction
        self.predict_tab = QWidget()
        self.predict_layout = QVBoxLayout()
        self.predict_tab.setLayout(self.predict_layout)
        self.tabs.addTab(self.predict_tab, "Predict")

        # Dictionary to store trained models
        self.trained_models = {}

        self.model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["ResNet50", "VGG16", "EfficientNetB0"])
        self.train_layout.addWidget(self.model_label)
        self.train_layout.addWidget(self.model_combo)

        self.split_label = QLabel("Train/Test Split (0.6, 0.7, 0.8):")
        self.split_input = QLineEdit("0.8")
        self.train_layout.addWidget(self.split_label)
        self.train_layout.addWidget(self.split_input)

        self.path_label = QLabel("Dataset Path:")
        self.path_input = QLineEdit("Assignment_3/data/dataset/training_set")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        self.train_layout.addWidget(self.path_label)
        self.train_layout.addWidget(self.path_input)
        self.train_layout.addWidget(self.browse_button)

        self.epochs_label = QLabel("Epochs:")
        self.epochs_input = QSpinBox()
        self.epochs_input.setRange(1, 100)
        self.epochs_input.setValue(1)
        self.train_layout.addWidget(self.epochs_label)
        self.train_layout.addWidget(self.epochs_input)

        self.start_button = QPushButton("Start Training")
        self.start_button.clicked.connect(self.run_training)
        self.train_layout.addWidget(self.start_button)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.train_layout.addWidget(self.canvas)

        # Prediction UI container
        container = QWidget()
        container.setMaximumWidth(500)
        container_layout = QVBoxLayout(container)

        # Image selection row
        self.img_label = QLabel("Upload Image:")
        self.img_path_input = QLineEdit()
        self.browse_img_button = QPushButton("Browse Image")
        self.browse_img_button.clicked.connect(self.browse_image)
        self.browse_img_button.setMaximumWidth(100)
        img_hbox = QHBoxLayout()
        img_hbox.addWidget(self.img_label)
        img_hbox.addWidget(self.img_path_input)
        img_hbox.addWidget(self.browse_img_button)
        container_layout.addLayout(img_hbox)

        # Model selection row
        self.predict_model_label = QLabel("Model:")
        self.predict_model_combo = QComboBox()
        self.predict_model_combo.addItems(["ResNet50", "VGG16", "EfficientNetB0"])
        self.predict_model_combo.setMaximumWidth(200)
        model_hbox = QHBoxLayout()
        model_hbox.addWidget(self.predict_model_label)
        model_hbox.addWidget(self.predict_model_combo)
        container_layout.addLayout(model_hbox)

        # Button row
        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(self.run_prediction)
        btn_hbox = QHBoxLayout()
        btn_hbox.addStretch()
        btn_hbox.addWidget(self.predict_button)
        btn_hbox.addStretch()
        container_layout.addLayout(btn_hbox)

        # Center container in the tab
        self.predict_layout.addStretch()
        self.predict_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.predict_layout.addStretch()

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
        QMessageBox.warning(self, "Alert", "Model is being trained, please wait...")
        model.fit(train_gen, validation_data=val_gen, epochs=epochs)

        # Store the trained model for later prediction
        self.trained_models[model_name] = model

        self.figure.clear()
        report_text = evaluate_model(model, val_gen, figure=self.figure)
        print(report_text)
        self.canvas.draw()
        formatted_report = (
            f"Cats:\n"
            f"  Precision: {report_text['cats']['precision']:.2f}\n"
            f"  Recall:    {report_text['cats']['recall']:.2f}\n"
            f"  F1-score:  {report_text['cats']['f1-score']:.2f}\n\n"
            f"Dogs:\n"
            f"  Precision: {report_text['dogs']['precision']:.2f}\n"
            f"  Recall:    {report_text['dogs']['recall']:.2f}\n"
            f"  F1-score:  {report_text['dogs']['f1-score']:.2f}\n\n"
            f"Accuracy:     {report_text['accuracy']:.2f}\n\n"
            f"Weighted Avg:\n"
            f"  Precision: {report_text['weighted avg']['precision']:.2f}\n"
            f"  Recall:    {report_text['weighted avg']['recall']:.2f}\n"
            f"  F1-score:  {report_text['weighted avg']['f1-score']:.2f}"
        )
        QMessageBox.information(self, "Classification Report", formatted_report)

    def browse_image(self):
        img_file, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg *.jpeg)")
        if img_file:
            self.img_path_input.setText(img_file)

    def run_prediction(self):
        model_name = self.predict_model_combo.currentText()
        if model_name not in self.trained_models:
            QMessageBox.critical(self, "Error", "Model not trained. Please train the model first.")
            return
        img_path = self.img_path_input.text()
        if not img_path:
            QMessageBox.critical(self, "Error", "Please select an image file.")
            return
        try:
            # Load and preprocess image
            from tensorflow.keras.preprocessing.image import load_img, img_to_array
            model = self.trained_models[model_name]
            input_shape = model.input_shape[1:3]
            img = load_img(img_path, target_size=input_shape)
            arr = img_to_array(img) / 255.0
            arr = np.expand_dims(arr, axis=0)
            preds = model.predict(arr)
            class_idx = np.argmax(preds[0])
            label = "Cat" if class_idx == 0 else "Dog"
            QMessageBox.information(self, "Prediction Result", f"Predicted animal: {label}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Prediction failed: {e}")
