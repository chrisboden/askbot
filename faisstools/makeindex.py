import json
import faiss
import numpy as np

# Load the embeddings from the JSON file
with open("embeds/test.json", "r") as f:
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
faiss.write_index(index, "embeds/test.index")

# Generate a random query vector with the same number of dimensions as the vectors in the index
query = np.random.random(len(X[0])).astype("float32")
query = query[np.newaxis, :]  # Add a new axis to make it a 2D array with a single row

# Query the index for the 10 nearest neighbors of the query vector
distances, indices = index.search(query, 10)

# Print the metadata for the nearest neighbors
for i in indices[0]:
    print(metadata[i])