import argparse
from utils import data_loader
from models import model_loader
from utils.metrics import evaluate_model

def main():
    print("🐶🐱 Dogs vs Cats Classifier\n")

    model_name = input("🔧 Wybierz model (ResNet50, VGG16, EfficientNetB0): ").strip()
    while model_name not in ['ResNet50', 'VGG16', 'EfficientNetB0']:
        model_name = input("❗ Niepoprawny model. Wybierz ponownie: ").strip()

    split = input("📊 Podaj podział trening/test (0.6, 0.7, 0.8) [domyślnie 0.8]: ").strip() or "0.8"
    while split not in ['0.6', '0.7', '0.8']:
        split = input("❗ Niepoprawny podział. Wybierz ponownie: ").strip()
    split = float(split)

    dataset_path = input("📁 Ścieżka do zbioru danych [domyślnie data/dataset/training_set]: ").strip() or "data/dataset/training_set"
    epochs = input("🔁 Liczba epok [domyślnie 5]: ").strip() or "5"
    epochs = int(epochs)

    # 🐾 Wczytywanie danych
    print(f"\n🔄 Ładowanie danych z {dataset_path} z podziałem {int(split*100)}/{int((1-split)*100)}...")
    train_gen, val_gen = data_loader.get_data_generators(dataset_path, split_ratio=split)

    # 🧠 Wczytywanie modelu
    print(f"📦 Wczytywanie modelu {model_name}...")
    model = model_loader.get_model(model_name)

    # 🚀 Trening
    print(f"🏋️ Rozpoczynanie treningu na {epochs} epok...")
    model.fit(train_gen, validation_data=val_gen, epochs=epochs)

    # 📊 Ewaluacja
    print("\n📈 Ewaluacja modelu:")
    evaluate_model(model, val_gen)

if __name__ == '__main__':
    main()
