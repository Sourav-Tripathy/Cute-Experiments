from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """
    A class to generate embeddings using the BAAI/bge-small-en-v1.5 model
    directly with the sentence-transformers library.
    """
    def __init__(self):
        """
        Initializes the EmbeddingGenerator and loads the model.
        """
        # Load the model directly using sentence-transformers
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")

    def get_embedding(self, text: str) -> list[float]:
        """
        Generates an embedding for the given text.

        Args:
            text: The input text to embed.

        Returns:
            A list of floats representing the embedding.
        """
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

if __name__ == '__main__':
    generator = EmbeddingGenerator()
    embedding = generator.get_embedding("This is a test sentence.")
    print(f"Generated embedding of dimension: {len(embedding)}")