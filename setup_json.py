# THis file is used to convert the base.csv file to base.json
# This is the required format for the faiss index

import csv
import json
import uuid

def csv_to_json(csv_file, json_file):
    # Open the CSV file and read in the rows
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Create an empty list to store the JSON objects
        json_objects = []

        # Initialize a counter
        row_count = 0

        # Iterate over the rows in the CSV file
        for row in csv_reader:
            # Increment the counter
            row_count += 1

            # Create a new JSON object using the template
            json_object = {
                "metadata": {
                    "id": str(uuid.uuid4()),
                    "contentAuthor": row['bookAuthor'],
                    "contentSource": row['bookTitle'],
                    "contentType": "book",
                    "quoteText": row['quoteText']
                },
                "values": [float(x) for x in row['contentEmbedding'][1:-1].split(',')]
            }
            # Add the JSON object to the list
            json_objects.append(json_object)

    # Open the JSON file and write the list of JSON objects to it
    with open(json_file, 'w') as json_file:
        json.dump({"vectors": json_objects}, json_file)

    # Print the count of rows in the CSV file
    csv_file_path = csv_file.name
    print(f"There are {row_count} rows in {csv_file_path}")

    # Print the count of records in the JSON file
    json_file_path = json_file.name
    print(f"There are {len(json_objects)} records in {json_file_path}")