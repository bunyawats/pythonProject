from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import URL, create_engine
from sqlalchemy import create_engine, inspect
from tabulate import tabulate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

pathDir = os.path.join(os.getcwd(), ".env")
print(pathDir)
load_dotenv(pathDir)
my_variable = os.getenv("LANGCHAIN_API_KEY")
print(my_variable)


url_object = URL.create(
    "postgresql+psycopg",
    username="gouser",
    password="A1u$35#24",  # plain (unescaped) text
    host="localhost",
    database="go",
)
engine = create_engine(url_object)

db = SQLDatabase(engine)

def get_schema(_):

    inspector = inspect(engine)
    columns = inspector.get_columns("customer")

    column_data = [
        {
            "Column Name": col["name"],
            "Data Type": str(col["type"]),
            "Nullable": "Yes" if col["nullable"] else "No",
            "Default": col["default"] if col["default"] else "None",
            "Autoincrement": "Yes" if col["autoincrement"] else "No",
        }
        for col in columns
    ]
    schema_output = tabulate(column_data, headers="keys", tablefmt="grid")
    formatted_schema = f"Schema for 'customer' table:\n{schema_output}"

    return formatted_schema


def run_query(query):
    return db.run(query)

print(get_schema("_"))


llm = OllamaLLM(model="llama3")

template = """
Based on the table schema below, write a SQL query that would answer the user's question. Just answer only pain SQL command:

{schema}

Question: {question}
SQL Query:"""
sql_prompt = ChatPromptTemplate.from_template(template)

sql_response = (
        RunnablePassthrough.assign(schema=get_schema)
        | sql_prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
)

template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(template)


def debug(input):
    print(">" * 150)
    print("SQL Output: ", input["query"])
    print(">" * 150)

    return input

sql_chain = (
    RunnablePassthrough.assign(query=sql_response).assign(
        schema=get_schema,
        response=lambda x: run_query(x["query"]),
    )
    | RunnableLambda(debug)
    | prompt_response
    | llm
    | StrOutputParser()
)

answer = sql_chain.invoke({"question": "Who is the oldest?"})
print(answer)