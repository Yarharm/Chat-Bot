# Chat-Bot

The following Chat-bot retrieves recipe information based on the request.

Typical use case:

    - Hello CookingMaster(Bot name)!
    - Hi there!
    - Get me a recipe for the noodle soup.
    - I found Asian Noodle Soup. You can check it out at: http://food2fork.com/view/47334

For the data processing and dialogue management Chat-bot uses an open-source [Rasa NLU](https://rasa.com/docs/nlu/) 
natural language processing tool.

Ingredients extraction is trained on the dataset from [Epicurious](https://www.kaggle.com/hugodarwood/epirecipes) Kaggle competition.
While the competition contains quite a substantial amount of ingredients, bot will not recognize ingredients that are not present in the dataset.

After the bot extracts all the ingredients, it searches for the recipes with a [Food2Fork](https://www.food2fork.com/about/api) API.

The whole Chat-bot application is integrated into Slack with [Slack API](https://api.slack.com/).
Application is actively listening on port 5004, while tunnel between Slack and App is created with [ngrok](https://ngrok.com/).