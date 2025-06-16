import json
from deep_translator import GoogleTranslator


with open('Assignment_2/data/recipes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


translator = GoogleTranslator(source='pl', target='en')


all_ingredients = set()
for recipe in data:
    all_ingredients.update(recipe['ingredients'])


translation_map = {}
for ingredient in all_ingredients:
    try:
        translated = translator.translate(ingredient)
        translation_map[ingredient] = translated
    except Exception as e:
        translation_map[ingredient] = f"[ERROR: {ingredient}]"
        print(f"Error translating '{ingredient}': {e}")


for recipe in data:
    recipe['ingredients_en'] = [translation_map[ing] for ing in recipe['ingredients']]


with open('recipes_translated.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)