import csv
import openai
import requests
import os
import shutil

def create_embeddings(input_csv_file):
  # Initialize the embeddings variable to an empty list
  embeddings = []

  # Set your API key and endpoint
  api_key = os.getenv("OPENAI_API_KEY") # Replace "YOUR_API_KEY" with your actual API key
  endpoint = "https://api.openai.com/v1/embeddings"

  # Open the input CSV file
  with open(input_csv_file, 'r') as f:
    # Read the contents of the CSV file into a list of dictionaries, where each dictionary represents a row in the CSV file
    rows = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

  # Iterate over each row in the input CSV file
  for row in rows:
    # Get the quote text, book title, and book author from the row
    quote_text = row['quoteText']
    book_title = row['bookTitle']
    book_author = row['bookAuthor']
    
    # Concatenate quote_text, book_title and book_author to create the "content" field
    content = f"{quote_text} | From: {book_title} | By: {book_author}"
    print(content)
    
    try:
      # Use the OpenAI API to create an embedding for the "content" field
      response = requests.post(endpoint, json={
        "model": "text-embedding-ada-002",
        "input": content
      }, headers={
        "Authorization": f"Bearer {api_key}"
      })
      if response.status_code != 200:
        # Print an error message if the API request failed
        print(f"Error creating embedding for content: {response.text}")
        continue
      try:
        content_embedding = response.json()["data"][0]["embedding"]
      except KeyError:
        # Print the entire response if the expected data is not present
        print(f"Unexpected response format for content embedding: {response.json()}")
        continue
    except Exception as e:
      # Print the error message if there is an exception
      print(f"An error occurred while calling the endpoint: {e}")
      continue

    # Create a dictionary to represent the row in the output CSV file
    embedding = {
      'quoteText': quote_text,
      'bookTitle': book_title,
      'bookAuthor': book_author,
      'contentEmbedding': content_embedding
    }

    # Add the embedding to the list of embeddings
    embeddings.append(embedding)

  # Set the output file path to 'embeds/new.csv'
  output_csv_file = 'data/main/base.csv'

  # Open the output CSV file in append mode
  with open(output_csv_file, 'a', newline='') as f:
    # Write the list of embeddings to the output CSV file
    writer = csv.DictWriter(f, fieldnames=['quoteText', 'bookTitle', 'bookAuthor', 'contentEmbedding'])
    
    # Don't write the header if the file already exists
    if f.tell() == 0:
        writer.writeheader()

    writer.writerows(embeddings)

    # Print a success message
    print("Done!")

def main():
  # Prompt the user for the input directory path
  input_dir = input("Enter the path to the input directory: ")

  # Iterate over each file in the input directory
  for file_name in os.listdir(input_dir):
    # Check if the file is a CSV file
    if file_name.endswith(".csv"):
      # Create the full file path
      file_path = os.path.join(input_dir, file_name)

      # Create embeddings for the file
      create_embeddings(file_path)

      # Move the file to the 'data/scrapes/complete' directory
      shutil.move(file_path, 'data/scrapes/complete')

if __name__ == '__main__':
  main()