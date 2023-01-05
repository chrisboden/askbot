import faiss
import numpy as np
from setup_index import index, metadata

# Variables to be edited
nr_of_results = 5

def searchq(index, query_embedding, metadata):
    # Convert the user embedding to a 2D numpy array
    query_embedding = np.array(query_embedding, dtype="float32")
    query_embedding = query_embedding[np.newaxis, :]  # Add a new axis to make it a 2D array with a single row

    # Query the index for the nearest neighbors of the query embedding
    distances, indices = index.search(query_embedding, nr_of_results)
    print(f"The matching indices are {indices}")

    # Return the metadata for the nearest neighbors
    return ["{}: {}".format(metadata[i]["contentAuthor"].strip("'"), metadata[i]["quoteText"].strip("'")) for i in indices[0]]