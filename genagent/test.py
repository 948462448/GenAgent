# template = """
#        ## BACKGROUND
#        Suppose you are {name}, you are in a debate with {opponent_name}.
#        ## DEBATE HISTORY
#        Previous rounds:
#        {context}
#        ## YOUR TURN
#        Now it's your turn, you should closely respond to your opponent's latest argument, state your position, defend your arguments, and attack your opponent's arguments,
#        craft a strong and emotional response in 80 words, in {name}'s rhetoric and viewpoints, your will argue:
#        """
# padding = {
#     "name": "Jim",
#     "opponent_name": "Bob",
#     "context": "Jim: I think you are right, because you are a good person.\nBob: I think you are wrong, because you are a bad person."
# }
# prompt = template.format(**padding)
# print(prompt)
# print(template)

"""


{
    "name": "Jim",
    "description": "You are a helpful assistant",
    "prompt": "",
    "role":"dpd",
    "interaction_type": "message"
}

"""
import inspect

from genagent.assistant.base_llm import BaseLLM
from genagent.assistant.llm_manager import LLM_MANGER
from genagent.memory.message import Message
from genagent.agent.agent import Agent

def main():
    json_str = """
        {
    "name": "Jim",
    "description": "You are a helpful assistant",
    "prompt": "",
    "role":"dpd",
    "interaction_type": "message"
}
    """
    agent = Agent.model_validate_json(json_str)
    message_str = """
         {
    "content": "hi",
    "send_from": "human",
    "send_to": "Jim",
    "role":"human"
}
    """
    message = Message.model_validate_json(message_str)
    response = agent.exec(message)
    print(response)


if __name__ == "__main__":
    main()
