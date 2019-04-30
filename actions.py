# Custom Actions

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from food2fork import Food2ForkClient

class ActionRecipe(Action):
    """
    Every Custom Action MUST inherit Rasa Class "Action"
    """
    def name(self):
        return 'action_recipe'  # Identical name in Domain.yml

    def run(self, dispatcher, tracker, domain):

        # Get Food2Fork Api Key
        with open('food_to_fork.txt') as keyFile:
            api_key = keyFile.readline()

        # Post request
        f2fClient = Food2ForkClient(api_key)
        recipe_ingredients = tracker.get_slot('ingredient')

        # Convert ingredient list to CS list
        query = ",".join(recipe_ingredients)

        response = f2fClient.search(query)

        # Parse Api response
        title = response['recipes'][0]['title']
        f2f_url = response['recipes'][0]['f2f_url']
        source_url = response['recipes'][0]['source_url']

        # Bot response
        response = 'I found {0}.\n' \
                   'You can check it out at food2fork website: {1},\n' \
                   'or at original source: {2}'.format(title, f2f_url, source_url)

        dispatcher.utter_message(response)
        return [SlotSet('ingredient', recipe_ingredients)]



