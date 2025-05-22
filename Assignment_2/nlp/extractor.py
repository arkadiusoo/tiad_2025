import json

def load_recipes(json_path="./data/recipes.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_ingredients(text, known_ingredients):
    words = text.lower().split()
    ingredients = [w for w in words if w in known_ingredients]
    return list(set(ingredients))

def filter_recipes(recipes, ingredients):
    return [r for r in recipes if all(i in r['ingredients'] for i in ingredients)]

def known_ingredients_set(recipes):
    return set(i for r in recipes for i in r['ingredients'])
