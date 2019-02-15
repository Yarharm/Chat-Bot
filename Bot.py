import logging
import pandas as pd
from database_manager import DbManager
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# Process logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


# Initialize the bot
bot = ChatBot(
    'Terminal',
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.db',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ]
)


# Get dataset
#data = pd.read_json('recipes.json')
#titles = data['title']
#titles = titles.dropna(axis=0)
#titles = titles.values

# Train bot
#trainer = ListTrainer(bot)
#trainer.train(titles)


# Initialize database manager
db_man = DbManager()

# Get database info
#db_man.get_db_content(bot, tables=False, storage=False)

# Train with corpus
def train_corpus(bot, corpus):
    # English corpus => "chatterbot.corpus.english"
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(corpus)

# Getting response
def bot_session(bot):
    while True:
        try:
            inp = input()
            bot_input = bot.get_response(inp)
            print(bot_input)

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

bot_session(bot)
#response = bot.get_response("what is your name?")
#print(response)
