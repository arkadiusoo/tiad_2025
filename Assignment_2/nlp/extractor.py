import json
import os

def load_recipes(json_path=None):
    if json_path is None:
        current_dir = os.path.join(os.path.dirname(__file__))
        json_path = os.path.join(current_dir, "../data/recipes_translated.json")
        json_path = os.path.abspath(json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_ingredients(text, known_ingredients):
    words = text.lower().split()
    ingredients = [w for w in words if w in known_ingredients]
    return list(set(ingredients))

def filter_recipes(recipes, ingredients, require_all=False):
    matching_recipes = []

    input_ingredients = set(ingredients)

    for recipe in recipes:
        recipe_ingredients = set(recipe['ingredients_en'])

        if require_all:
            if recipe_ingredients.issubset(input_ingredients):
                matching_recipes.append((len(recipe_ingredients), recipe))
        else:
            matched = recipe_ingredients & input_ingredients
            if matched:
                matching_recipes.append((len(matched), recipe))

    matching_recipes.sort(reverse=True, key=lambda x: x[0])
    return [recipe for _, recipe in matching_recipes]

def known_ingredients_set(recipes):
    print(set(i for r in recipes for i in r['ingredients_en']))
    return set(i for r in recipes for i in r['ingredients_en'])
