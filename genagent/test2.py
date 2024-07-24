# from genagent.assistant.base_llm import BaseLLM
#
# subclasses = BaseLLM.__subclasses__()
# for subclass in subclasses:
#     print(subclass.__name__)
# class Foo(object): pass
# class Bar(Foo): pass
# class Baz(Foo): pass
# class Bing(Bar): pass
from genagent.assistant import BaseLLM

print([cls.__name__ for cls in BaseLLM.__subclasses__()])