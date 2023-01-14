import os
import openai
import dotenv

config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

def get_embedding(text):
  openai.api_key = os.getenv("OPENAI_API_KEY")
  response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=text
  )
  embedding = response["data"][0]["embedding"]
  return embedding
  print(f"The query embedding is {embedding}")