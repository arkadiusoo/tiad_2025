from Assignment_2.audio import recorder
from Assignment_2.nlp import extractor


def main():
    file_path = input("Podaj ścieżkę do pliku audio: ").strip()
    text = recorder.recognize_audio(file_path, "pl-PL")
    recipes = extractor.load_recipes()
    known = extractor.known_ingredients_set(recipes)
    ingredients = extractor.extract_ingredients(text, known)
    matches = extractor.filter_recipes(recipes, ingredients)
    print("Dopasowane przepisy")
    if matches:
        for recipe in matches:
            print(f"- {recipe['name']} ({', '.join(recipe['ingredients'])})")
    else:
        print("Brak dopasowanych przepisów.")

if __name__ == "__main__":
    main()
