from langchain import hub
import os

my_variable = os.getenv('LANGCHAIN_API_KEY')
print(my_variable)
prompt = hub.pull("rlm/rag-prompt")

print(prompt)