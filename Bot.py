# Initialize bot and listen on port 5004

from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import yaml
from rasa_core.utils import EndpointConfig


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/grandmarecipes')
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('./models/dialogue', interpreter=nlu_interpreter, action_endpoint=action_endpoint)

# Get Slack bot verification token
with open('slack_bot_verification.txt') as verificationFile:
    bot_token = verificationFile.readline()
input_channel = SlackInput(bot_token)
agent.handle_channels([input_channel], 5004, serve_forever=True)