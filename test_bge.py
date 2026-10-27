from app.nlp.embeddings import SemanticEmbedder
embedder = SemanticEmbedder()
emb = embedder.get_embedding("Testing BGE model")
print("Embedding generated, shape:", emb.shape)
