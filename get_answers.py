import faiss
import numpy as np
from setup_index import index, metadata
import json
from pathlib import Path
import sqlite3

# Set up the various file path variables so that the paths are relative no matter the environment
cwd = Path(__file__).parent.resolve()
data_path = cwd.joinpath('data', 'main')
json_path = data_path.joinpath('base.json')


# Variables to be edited
nr_of_results = 5


def searchq(index, query_embedding, database_path):
    # Convert the user embedding to a 2D numpy array
    query_embedding = np.array(query_embedding, dtype="float32")
    query_embedding = query_embedding[np.newaxis, :]  # Add a new axis to make it a 2D array with a single row

    # Query the index for the nearest neighbors of the query embedding
    distances, indices = index.search(query_embedding, nr_of_results)

    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(metadata);")
    print(cursor.fetchall())


    # Fetch the metadata for the nearest neighbors
    metadata = []
    for i in indices[0]:
        select_stmt = "SELECT contentAuthor, quoteText FROM metadata WHERE id={}".format(i)
        print(select_stmt)
        cursor.execute(select_stmt)
        result = cursor.fetchone()
        if result is not None:
            metadata.append("{}: {}".format(result[0], result[1]))

    print(f"The indices are {indices}")
    print(f"The metadata is {metadata}")

    # Close the connection
    conn.close()

    return metadata