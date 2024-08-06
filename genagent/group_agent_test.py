from genagent.agent.agent import Agent
from genagent.group.group import Group
from genagent.memory.message import Message

json_1_str = """
        {
    "name": "Jim",
    "description": "你的名字叫吉姆，你是一个喜剧二人组的一员。",
    "prompt": "",
    "tools":[],
    "role":"",
    "interaction_type": "message",
    "mode":"multi"
}
    """
agent_1 = Agent.model_validate_json(json_1_str)
json_2_str = """
        {
    "name": "dede",
    "description": "你的名字叫得得，你是一个喜剧二人组的一员。",
    "prompt": "",
    "tools":[],
    "role":"",
    "mode":"multi",
    "interaction_type": "message",
    "next":"Jim"
}
    """
agent_2 = Agent.model_validate_json(json_2_str)
group_json = """
{
"name": "喜剧表演",
"description":"这是一个非常好笑的喜剧表演",
"maximum_dialog_rounds": 4
}
"""
group = Group.model_validate_json(group_json)
group.add_group(agent_1)
group.add_group(agent_2)
message = Message(content="得得你好啊，能给我讲一个笑话吗？", send_to="dede", send_from="Jim")
group.run(message)