import sqlite3
from sqlite3 import Error
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


# Initialize the bot
cb = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db'
)

# Training conversation
conversation = [
    'How many boys are in Ukraine?',
    'There are two boys: Vadim and Taras'
]

# Train step
#trainer = ListTrainer(cb)
#trainer.train(conversation)

# Getting response
#while True:
#    try:
#        bot_input = cb.get_response(input())
#        print(bot_input)

#    except(KeyboardInterrupt, EOFError, SystemExit):
#        break

# Connect to sqlite
db = './database.db'
try:
    conn = sqlite3.connect(db)
except Error as e:
    print(e)

# Create cursor
cur = conn.cursor()
cur.execute("select name from sqlite_master where type = 'table';")

tables = cur.fetchall()
for table in tables:
    print(table)