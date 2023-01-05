import faiss
import pandas as pd

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("embeds/base.csv")

# Extract the embeddings from the DataFrame
embeddings = df["contentEmbedding"].values

# Create an IVF index with 64-bit float vectors and 256 coarse quantizer centroids
index = faiss.IndexIVFFlat(faiss.VectorTransform(embeddings.shape[1]), 256, faiss.METRIC_INNER_PRODUCT)

# Train the index on the embeddings
index.train(embeddings)

# Add the embeddings to the index
index.add(embeddings)

# Perform a vector search query
query = [0.1, 0.2, 0.3]  # this is just an example query vector
k = 10  # number of results to return
results, distances = index.search(query, k)

# Print the indices and distances of the nearest neighbors
print(results)
print(distances)