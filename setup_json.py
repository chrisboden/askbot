import csv
import json
import uuid
from pathlib import Path
from ast import literal_eval

def csv_to_json(csv_file, json_file):
    # Convert the file paths to strings if they are Path objects
    csv_file = str(csv_file)
    json_file = str(json_file)

    # Open the CSV file and read in the rows
    with open(csv_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)


        # Create an empty list to store the JSON objects
        json_objects = []

        # Initialize a counter
        row_count = 0

        # Iterate over the rows in the CSV file
        for index, row in enumerate(csv_reader):
            json_object = {
                "metadata": {
                    "id": index,
                    "contentAuthor": row['bookAuthor'],
                    "contentSource": row['bookTitle'],
                    "contentType": "book",
                    "quoteText": row['quoteText']
                },
                "values": literal_eval(row['contentEmbedding'])
            }
            json_objects.append(json_object)


    # Open the JSON file and write the list of JSON objects to it
    with open(json_file, 'w', encoding='utf-8') as json_file:
        json.dump({"vectors": json_objects}, json_file, ensure_ascii=False)

    # Print the count of rows in the CSV file
    csv_file_path = csv_file.name
    print(f"There are {row_count} rows in {csv_file_path}")

    # Print the count of records in the JSON file
    json_file_path = json_file.name
    print(f"There are {len(json_objects)} records in {json_file_path}")
