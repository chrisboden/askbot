import csv
import json
import os
from pathlib import Path

# Set the path to the directory containing the csv files
csv_dir = Path('data/scrapes/complete')

# Set the path to the json file
json_file = Path('data/main/sources.json')

# Initialize an empty list to store the data
data = []

# Iterate through the csv files in the directory
for filename in os.listdir(csv_dir):
  # Check if the file is a csv file
  if filename.endswith('.csv'):
    # Open the csv file
    with open(os.path.join(csv_dir, filename)) as f:
      # Create a DictReader object to read the csv file
      reader = csv.DictReader(f)
      # Initialize variables to store the bookAuthor, bookTitle, and quoteTotal data
      book_author = ''
      book_title = ''
      quote_total = 0
      # Iterate through the rows in the file
      for row in reader:
        # Increment the quote total
        quote_total += 1
        # Extract the bookAuthor and bookTitle data from the first row
        if quote_total == 1:
          book_author = row['bookAuthor']
          book_title = row['bookTitle']
      # Create a dictionary with the required data
      quote_data = {
        'fileName': filename,
        'bookAuthor': book_author,
        'bookTitle': book_title,
        'quoteTotal': quote_total - 1 # Subtract 1 to exclude the header row
      }
      # Add the data to the list
      data.append(quote_data)

# Write the data to the json file
with open(json_file, 'w') as f:
  json.dump(data, f, indent=2)