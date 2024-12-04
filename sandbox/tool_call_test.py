import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from sympy.polys.polyconfig import query

pathDir = os.path.join(os.getcwd(), ".env")
# print(pathDir)
load_dotenv(pathDir)

def compose_tool_call_output(input: dict):
    print(input["ai_msg"].tool_calls)
    print(">>" * 50)
    input["messages"].append(input["ai_msg"])
    for tool_call in input["ai_msg"].tool_calls:

        selected_tool = {
            "add": add,
            "multiply": multiply,
            "get_boss_detail": get_boss_detail
        }[tool_call["name"].lower()]

        tool_msg = selected_tool.invoke(tool_call)
        input["messages"].append(tool_msg)

    return input["messages"]

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""

    return a * b

@tool
def get_boss_detail() -> str:
    """
    Useful for get boss detail.
    Boss 's thai name = fname + lname
    Boss 's english name = efname + elname
    Boss 's photo = picture

    :return: Boss Name
    """

    return "Bunyawat Singchai"


def query_llm(chat_query : str, company_id : str, user_token: str) -> str:

    llm = ChatOllama(model="llama3.1", temperature=0, )

    tools = [add, multiply, get_boss_detail]
    llm_with_tools = llm.bind_tools(tools)

    chain = (RunnableLambda(lambda x: [HumanMessage(x)])
             | {"ai_msg": RunnablePassthrough() | llm_with_tools, "messages": RunnablePassthrough()}
             | RunnableLambda(compose_tool_call_output)
             | llm_with_tools
             | StrOutputParser())
    return chain.invoke(chat_query)

# query = "What is 3 * 12? Also, what is 11 + 49?"
# chat_query = "WHo is my boss"
# print(chain.invoke(chat_query))
