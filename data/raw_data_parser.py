import json
import pandas as pd
import os

# Get Recipe texts
#recipe_text = pd.read_csv(os.getcwd() + '/raw_data/recipes.csv', low_memory=False)
#recipe_text = recipe_text['title']
# print(recipe_text.shape)
# print(recipe_text[0])
class RawDataParser:
    """
    Every recipe and ingredient processed as *Lowercase*
    """
    def __init__(self):
        self.recipes = os.getcwd() + '/raw_data/recipes.csv'
        self.ingredients = os.getcwd() + '/raw_data/ingredients.json'
        self.LEFT_CURLY = '{'
        self.RIGHT_CURLY = '}'

    def get_recipes_list(self):
        """
        Get list of recipe requests
        :return:
        """
        recipes_text = pd.read_csv(self.recipes, low_memory=False)
        recipes_text = recipes_text['title']
        recipes_text = recipes_text.map(lambda x: x.lower())
        result_lst = list(dict.fromkeys(recipes_text.to_list()))

        # Remove recipes with no entities
        no_entities_recipes = self.get_no_entities_recipes(result_lst, self.get_ingredient_list())
        for index, recipe in enumerate(result_lst):
            if recipe in no_entities_recipes:
                result_lst.pop(index)
        return result_lst

    def get_ingredient_list(self):
        """
        Get list of most common ingredients for entity extraction
        :return: return list of unique ingredient names
        """
        result_ingredients_lst = []
        with open(self.ingredients) as json_file:
            ingrdnts = json.load(json_file)
            for object in ingrdnts:
                if 'categories' in object:
                    result_ingredients_lst.extend([x.lower() for x in object['categories']])
        return list(dict.fromkeys(result_ingredients_lst))

    def get_entities_from_recipe(self, recipe, ingredient_lst):
        """
        Get entities from the recipe.
        return dictionary of entities (key) : start index of entity in recipe (value)
        :param recipe: recipe string
        :param ingredient_lst: list of ingredients (entities)
        :return: return dictionary of recipes
        """
        resultDict = {}
        for entity in ingredient_lst:
            # If entity is a substring of the recipe
            if entity in recipe:
                resultDict[entity] = recipe.find(entity)
        return resultDict

    def write_interpreter_object(self):

    def get_no_entities_recipes(self, recipes, ingredients):
        useless = {}
        for recipe in recipes:
            result = self.get_entities_from_recipe(recipe, ingredients)
            if len(result) == 0:
                useless[recipe] = True
        return useless

parser = RawDataParser()
recipes = parser.get_recipes_list()
ingr = parser.get_ingredient_list()


