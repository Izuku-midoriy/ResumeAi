import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticEmbedder:
    """Handles text embeddings using sentence-transformers."""
    
    def __init__(self, model_name='BAAI/bge-base-en-v1.5'):
        # This will download the model weights the first time it is run
        # Retained 'all-MiniLM-L6-v2' as a baseline configurable option.
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text):
        """Generate a dense vector embedding for the given text."""
        if not text or not isinstance(text, str):
            text = ""
        # The model returns a numpy array
        # normalize_embeddings=True is recommended for BAAI/bge-base-en-v1.5
        return self.model.encode(text, normalize_embeddings=True)

    def calculate_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings."""
        # Reshape for sklearn cosine_similarity which expects 2D arrays
        vec1 = np.array(embedding1).reshape(1, -1)
        vec2 = np.array(embedding2).reshape(1, -1)
        return float(cosine_similarity(vec1, vec2)[0][0])
