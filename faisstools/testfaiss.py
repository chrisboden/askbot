import faiss
import io
import numpy as np

with open('embeds/vector.index', 'rb') as f:
    index = faiss.index(np.load(f))
    print(index.d)  # prints the number of dimensions in the index
    print(index.ntotal)  # prints the total number of vectors in the index