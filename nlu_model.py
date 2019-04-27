# Prepare Rasa Interpreter (models/nlu)

from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
import os

def train_nlu(data, configs, model_dir):
    training_data = load_data(data)
    trainer = Trainer(config.load(configs))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name='grandmarecipes')

if __name__ == '__main__':
    if not os.path.isdir(os.getcwd() + "/models"):
        train_nlu('./data/data.json', 'config_spacy.json', './models/nlu')