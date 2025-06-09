# Dogs vs. Cats Image Classification

This project focuses on object recognition in images using deep learning models implemented with TensorFlow and Keras. We utilize the "Dogs & Cats Images" dataset available on Kaggle, aiming to classify images into two categories: dogs and cats.

## 📊 Project Scope (Grade 5 Criteria)

The project meets all criteria required for the highest grade, including:

1. Evaluation of three distinct classification models:
   - ResNet50
   - VGG16
   - EfficientNetB0

2. Performance comparison for different training/testing data splits:
   - 80% / 20%
   - 70% / 30%
   - 60% / 40%

3. Evaluation based on standard classification metrics:
   - Confusion Matrix
   - Accuracy
   - Precision
   - Recall
   - F1-Score

4. Visualization of model performance using ROC curves (via `scikit-learn`).

## 📁 Dataset

- **Source**: [Dogs & Cats Images – Kaggle](https://www.kaggle.com/datasets/chetankv/dogs-cats-images/data)
- **Classes**: Binary classification – Dog / Cat
- **Preprocessing**:
  - Resizing to 224x224 pixels
  - Normalization
  - Train/test split

## 🖥️ Graphical User Interface (GUI)

A graphical interface is implemented using **PyQt6**, allowing users to:
- Select and preview input images
- Choose between classification models
- View predicted labels and classification confidence
- Display evaluation metrics and visualizations interactively

## 🛠️ Technologies Used

- Python
- TensorFlow
- Keras
- scikit-learn
- PyQt6
- matplotlib / seaborn

## 🧪 Model Evaluation

Each model is trained and evaluated on all defined data splits. We provide:
- Confusion matrices for visual assessment
- Metric-based comparisons
- ROC curves to evaluate classifier discrimination

## 📈 Results

We summarize and compare the models based on accuracy and robustness to data split variations. This allows us to identify the most reliable architecture for binary image classification in this context.

## 🚀 How to Run

1. Download and unzip the dataset from Kaggle.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the GUI application:
   ```bash
   python main.py
   ```
4. Evaluation results and plots will be displayed in the interface and saved to the `results/` directory.

## 📎 License

This project is intended for academic use only.
