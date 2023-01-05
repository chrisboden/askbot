import os
import openai

def get_embedding(text):
  openai.api_key = os.getenv("OPENAI_API_KEY")
  response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=text
  )
  embedding = response["data"][0]["embedding"]
  return embedding
  print(f"The query embedding is {embedding}")