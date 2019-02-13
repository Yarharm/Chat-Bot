import logging
import os
from database_manager import DbManager
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# Process logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


# Initialize the bot
bot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.db'
)
# Initialize database manager
db_man = DbManager()
db_man.get_db_content(bot, tables=False, storage=False)

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


#response = bot.get_response("what is your name?")
#print(response)
