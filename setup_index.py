# This file handles the data setup for the app
# It converts the base.csv to base.json then creates the faiss index. These files live in /embeds dir
import json
import faiss
import numpy as np
from pathlib import Path

# Import the function that converts the CSV to JSON from makejson.py
from setup_json import csv_to_json

# Convert the base.csv to base.json
csv_to_json(Path('data/main/base.csv'), Path('data/main/base.json'))

# Load the embeddings from the JSON file
with open(Path("data/main/base.json"), "r") as f:
    data = json.load(f)

# Extract the embeddings and metadata from the JSON file
X = [vector["values"] for vector in data["vectors"]]
metadata = [vector["metadata"] for vector in data["vectors"]]

# Convert the list of lists to a 2D numpy array
X = np.array(X, dtype="float32")

# Create a FAISS index using the Euclidean distance metric
index = faiss.IndexFlatL2(len(X[0]))

# Add the vectors to the index
index.add(X)

# Save the index to a file
faiss.write_index(index, str(Path("data/main/base.index")))


metadata_count=len([item for item in metadata if "id" in item])
print(f"There are {metadata_count} metadata items")