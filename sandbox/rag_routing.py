from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel

from sandbox.langchain_sql_executor import sql_chain
from sandbox.rag_pgvector_query import rag_chain

classification_template = PromptTemplate.from_template(
    """You are good at classifying a question.
    Given the user question below, classify it as either being about `Database`, `Chat` or 'Offtopic'.
    Please answer only classified words and no surrounding quote

    <If the question is about someone attributes classify the question as 'Database'>
    <If the question is about content in the document, classify it as 'Chat'>
    <If the question is about whether, football or anything else not related to the people or operation on the ship, classify the question as 'offtopic'>

    <question>
    {question}
    </question>

    Classification:"""
)

def route(info):
    if "database" in info["topic"].lower():
        return sql_chain
    elif "chat" in info["topic"].lower():
        return rag_chain
    else:
        return "I am sorry, I am not allowed to answer about this topic."

classification_chain = classification_template | OllamaLLM(model="llama3") | StrOutputParser()

full_chain = RunnableParallel(
    {
        "topic": classification_chain,
        "question": lambda x: x["question"],
    }
) | RunnableLambda(route)

result = full_chain.invoke({"question": "How old is Bunyawat?"})

print(">" * 150)
print(result)
print(">" * 150)

# result = full_chain.invoke({"question": "แสดง สารบัญ ของเอกสารนี้?"})
# print(result)
