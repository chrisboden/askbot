from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA

with open('embeds/test.csv') as f:
    quotes = f.read()
texts = quotes

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)

qa = VectorDBQA.from_llm(llm=OpenAI(), vectorstore=docsearch)

query = "What did the president say about Ketanji Brown Jackson"
qa.run(query)