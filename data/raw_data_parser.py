import json
import pandas as pd
import os

class RawDataParser:
    """
    Parse for recipes and ingredients from the Kaggle challenge at:
        'https://www.kaggle.com/hugodarwood/'
    And write processed results to the data.json for the Rasa NLU Interpreter

    NOTE: Every recipe and ingredient processed as *Lowercase* only
    """
    def __init__(self):
        self.recipes = os.getcwd() + '/raw_data/recipes.csv'
        self.ingredients = os.getcwd() + '/raw_data/ingredients.json'
        self.greet_goodbye = os.getcwd() + '/raw_data/greet_goodbye.json'

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

    def process_recipe(self, recipe, entities_info):
        """
        Process recipe example to match Rasa NLU style
        """
        entities_processed = []
        single_entity = {}
        for entity, entity_start_index in entities_info.items():
            single_entity["start"] = entity_start_index
            single_entity["end"] = entity_start_index + len(entity)
            single_entity["value"] = entity
            single_entity["entity"] = "ingredient"
            entities_processed.append(single_entity)
            single_entity = {}

        single_recipe_processed = {"text": recipe,
                                   "intent": "inform",
                                   "entities": entities_processed}
        return single_recipe_processed

    def write_processed_info(self):
        # Prepare json file for Rasa Interpreter
        MAIN_FILE = {}
        COMMON_EXAMPLES = {}
        processed_objects = []
        MAIN_FILE["rasa_nlu_data"] = COMMON_EXAMPLES
        COMMON_EXAMPLES["common_examples"] = processed_objects

        # Add greet/goodbye information
        with open(self.greet_goodbye) as json_f:
            greet_bye_info = json.load(json_f)
            processed_objects.extend(greet_bye_info["first_layer"]["second_layer"])

        # Get data
        recipes = self.get_recipes_list()
        ingredients = self.get_ingredient_list()
        for index, recipe in enumerate(recipes):
            entities_info = self.get_entities_from_recipe(recipe, ingredients)
            recipe_processed = self.process_recipe(recipe, entities_info)

            # Add to the processed object wrapper
            processed_objects.append(recipe_processed)

        # Write data
        with open(os.getcwd() + '/data.json', 'w') as outfile:
            json.dump(MAIN_FILE, outfile, indent=2)

    def get_no_entities_recipes(self, recipes, ingredients):
        useless = {}
        for recipe in recipes:
            result = self.get_entities_from_recipe(recipe, ingredients)
            if len(result) == 0:
                useless[recipe] = True
        return useless

parser = RawDataParser()
parser.write_processed_info()
