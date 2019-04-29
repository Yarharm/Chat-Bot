# Interactive training script

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.train import interactive
from rasa_core.utils import EndpointConfig

logger = logging.getLogger(__name__)


def run_recipe_online(interpreter,
                      domain_file="recipes_domain.yml",
                      training_data_file="data/stories.md"):

    # Set up endpoint for Custom Action
    # NOTE: Custom Actions run on a separate server
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")

    # Create Agent
    # NOTE: Agent processes stories and uses Rasa Interpreter for input analysis
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=5),
                            KerasPolicy(max_history=5, epochs=6, batch_size=150)],
                  interpreter=interpreter, action_endpoint=action_endpoint)

    # Train agent
    data = agent.load_data(training_data_file)
    agent.train(data)
    interactive.run_interactive_learning(agent, training_data_file)

    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/grandmarecipes')
    run_recipe_online(interpreter=nlu_interpreter)
