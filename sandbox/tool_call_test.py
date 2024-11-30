from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_ollama import ChatOllama


pathDir = os.path.join(os.getcwd(), ".env")
# print(pathDir)
load_dotenv(pathDir)

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


def composToolCallOutput( ai_msg ) :
    print(ai_msg.tool_calls)

    print(">>" * 100)

    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    return messages


tools = [add, multiply]

llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12? Also, what is 11 + 49?"
messages = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)

messages = composToolCallOutput(ai_msg)
print(llm_with_tools.invoke(messages))

# tool_chain = llm_with_tools | RunnableLambda(composToolCallOutput) | llm_with_tools | StrOutputParser
#
# print( tool_chain.invoke([HumanMessage("What is 3 * 12? Also, what is 11 + 49?")]) )