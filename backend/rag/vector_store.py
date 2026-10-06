import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class VectorStore:

    def __init__(self):

        self.embedding_model = (
            SentenceTransformer(
                MODEL_NAME
            )
        )

        self.client = chromadb.PersistentClient(
            path="data/vectorstore"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="autohld"
            )
        )


    def reset(self) -> None:
        """
        Clear the current HLD index.
        """

        try:

            self.client.delete_collection(
                "autohld"
            )

        except Exception:
            pass

        self.collection = (
            self.client.get_or_create_collection(
                name="autohld"
            )
        )


    def add_chunks(
        self,
        chunks: list[dict]
    ) -> None:

        if not chunks:
            return

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = (
            self.embedding_model.encode(
                documents,
                normalize_embeddings=True
            ).tolist()
        )

        ids = [
            f"page_{chunk['page']}_"
            f"chunk_{index}"
            for index, chunk in enumerate(
                chunks
            )
        ]

        metadatas = [
            {
                "page": chunk["page"],
                "section": (
                    chunk.get("section")
                    or "Unknown"
                )
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )


    def search(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        query_embedding = (
            self.embedding_model.encode(
                [query],
                normalize_embeddings=True
            ).tolist()
        )

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        matches = []

        for i, document in enumerate(
            results["documents"][0]
        ):

            metadata = (
                results["metadatas"][0][i]
            )

            matches.append({
                "text": document,
                "page": metadata["page"],
                "section": metadata["section"],
                "distance": (
                    results["distances"][0][i]
                )
            })

        return matches