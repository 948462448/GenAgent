import json

from genagent.agent.agent import Agent
from genagent.assistant import LLMConfig
from genagent.group.group import Group
from genagent.memory.message import Message

json_1_str = """
        {{
    "name": "Jim",
    "description": "你的名字叫吉姆，你是一个相声演员",
    "system_prompt": "你的名字叫吉姆，你是一个相声搭档中的一员。你现在作为捧哏，需要跟你的搭档得得，给大家表演一场相声表演，你仅需要回答吉姆的台词即可",
    "prompt": "尽量不要与上下文中提供的历史对话记录重复",
    "tools":[],
    "role":"",
    "interaction_type": "message",
    "mode":"multi",
    "llm_config": {llm_config},
    "next":"dede"
}}
    """

json_2_str = """
        {{
    "name": "dede",
    "description": "你的名字叫得得，你是一个相声演员。",
    "system_prompt": "你的名字叫得得，你是一个相声搭档中的一员。你现在作为逗哏，需要跟你的搭档吉姆，给大家表演一场相声表演.你仅需要回答得得的台词即可",
    "prompt": "尽量不要与上下文中提供的历史对话记录重复",
    "tools":[],
    "role":"",
    "mode":"multi",
    "llm_config": {llm_config},
    "interaction_type": "message",
    "next":"Jim"
}}
    """
group_llm_config = LLMConfig(
    openai_api_key="sk-0da03bdfd5414766ae05a0050134cfb1",
    openai_base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=1.5,
    frequency_penalty=1.5,
    presence_penalty=1.5,
    is_json=True)
agent_llm_config = LLMConfig(
    openai_api_key="sk-0da03bdfd5414766ae05a0050134cfb1",
    openai_base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=1.5,
    frequency_penalty=1.5,
    presence_penalty=1.5,
    is_json=False)
agent_1 = Agent.model_validate_json(json_1_str.format(llm_config=json.dumps(agent_llm_config.__dict__)))
agent_2 = Agent.model_validate_json(json_2_str.format(llm_config=json.dumps(agent_llm_config.__dict__)))
group_json = """
{{
"name": "相声表演",
"description":"这是一场好笑的相声表演",
"maximum_dialog_rounds": 10,
"llm_config": {llm_config}
}}
"""
str1 = json.dumps(group_llm_config.__dict__)
group = Group.model_validate_json(group_json.format(llm_config=str1))
group.add_group(agent_1)
group.add_group(agent_2)
message = Message(content="吉姆，咱俩一起给观众表演一段主题是爆笑的相声怎么样？咱俩互相给对方讲段子。你先开始吧", send_to="Jim", send_from="dede")
group.run(message)