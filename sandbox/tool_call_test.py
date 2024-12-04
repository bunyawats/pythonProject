import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from sandbox.call_rest_service import call_boss_detail

pathDir = os.path.join(os.getcwd(), ".env")
load_dotenv(pathDir)

global_company_id = ""
global_user_token = ""

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

    company_id = "eb2f4f30-edaf-11ee-a69a-c7680edc0e47"
    user_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzY2hlbWEiOiJkYm8iLCJlbmNvZGUiOiIyIiwic3ViIjoiQXV0aCIsImNvbXBhbnlOYW1lIjoi4Lia4Lij4Li04Lip4Lix4LiXIOC4oeC4suC4ouC5gOC4reC4iuC4reC4suC4o-C5jCDguIjguLPguIHguLHguJQiLCJkYk5hbWUiOiJNWUhSUExVUyIsInJvbGVzIjpbIlVTRVIiXSwid29ya2FyZWEiOiJUS1ciLCJpc3MiOiJDb21wdXRlciBTY2llbmNlIENvcnBvcmF0aW9uIExpbWl0ZWQiLCJ6bWxvZ2luIjoiZmFsc2UiLCJyb2xlX2xldmVsIjoiNiIsImVtcGxveWVlaWQiOiIxMDAwMDA4MiIsImJyYW5jaCI6Im15aHIiLCJlbXBfcG9zaXRpb24iOiIwOTciLCJ1c2VyX3JvbGUiOiJBbGwiLCJ1aWQiOiIxMDAwMDA4MiIsImNvbXBhbnlpZCI6IjEwMCIsImFjdG9yaWQiOiIxMDAwMDA4MiIsImxhbmciOiJ0aCIsImFkIjoiZmFsc2UiLCJmaXJzdGxvZ2luIjoiZmFsc2UiLCJ1cmxfbXlociI6Imh0dHA6Ly9ocnBsdXMtc3RkLm15aHIuY28udGgvaHIiLCJhcHBfbmFtZSI6Im15aHIiLCJyZWdpb25hbGx0eSI6IkVORyIsInRva2VuX3plZW1lIjoiIiwidXNlcl9sZXZlbCI6Ik1ZSFIiLCJmdWxsbmFtZSI6IuC4meC4suC4ouC4reC4nuC4tOC4o-C4seC4leC4meC5jCAg4LiX4LiU4Liq4Lit4LiaIiwiY29taWQiOiIiLCJqb2IiOiIwOTctMjQ2OSIsInVzZXIiOiJteWhyIiwiem1fdXNlciI6IiIsInVzZXJuYW1lIjoibXlociIsIm1lbWJlcmlkIjoiIn0.R70ZQ1_HPA1pq-jeyxD-K4eKZKLYVIg2jmFDhenQjQc"

    return call_boss_detail(company_id, user_token)

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
