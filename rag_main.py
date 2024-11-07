

from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3")
ans = model.invoke("Come up with 10 names for a song about parrots")

print(ans)

from langchain_community.document_loaders import PDFPlumberLoader
loader = PDFPlumberLoader("11pests1disease.pdf")
docs = loader.load()

# Check the number of pages
print("Number of pages in the PDF:",len(docs))

# Load the random page content
print(docs[2].page_content)