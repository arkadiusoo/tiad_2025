import argparse
from utils import data_loader
from models import model_loader
from utils.metrics import evaluate_model

def main():
    # 🧾 Argumenty z linii komend
    parser = argparse.ArgumentParser(description="Dogs vs Cats Classifier")
    parser.add_argument('--model', type=str, choices=['ResNet50', 'VGG16', 'EfficientNetB0'], required=True)
    parser.add_argument('--split', type=float, choices=[0.6, 0.7, 0.8], default=0.8)
    parser.add_argument('--dataset_path', type=str, default="data/dogs-cats-images/training_set")
    parser.add_argument('--epochs', type=int, default=5)
    args = parser.parse_args()

    # 🐾 Wczytywanie danych
    print(f"\n🔄 Ładowanie danych z {args.dataset_path} z podziałem {int(args.split*100)}/{int((1-args.split)*100)}...")
    train_gen, val_gen = data_loader.get_data_generators(args.dataset_path, split_ratio=args.split)

    # 🧠 Wczytywanie modelu
    print(f"📦 Wczytywanie modelu {args.model}...")
    model = model_loader.get_model(args.model)

    # 🚀 Trening
    print(f"🏋️ Rozpoczynanie treningu na {args.epochs} epok...")
    model.fit(train_gen, validation_data=val_gen, epochs=args.epochs)

    # 📊 Ewaluacja
    print("\n📈 Ewaluacja modelu:")
    evaluate_model(model, val_gen)

if __name__ == '__main__':
    main()
