from backend.rag.vector_store import VectorStore


class RAGService:

    def __init__(self):

        self.vector_store = VectorStore()


    def retrieve_context(
        self,
        question: str,
        top_k: int = 3
    ) -> list[dict]:

        return self.vector_store.search(
            question,
            top_k=top_k
        )


    def build_context(
        self,
        results: list[dict]
    ) -> str:

        context_parts = []

        for result in results:

            section = (
                result.get("section")
                or "Unknown section"
            )

            context_parts.append(
                f"[Page {result['page']} | "
                f"Section: {section}]\n"
                f"{result['text']}"
            )

        return "\n\n".join(
            context_parts
        )


    def prepare_question(
        self,
        question: str,
        top_k: int = 3
    ) -> dict:

        results = self.retrieve_context(
            question,
            top_k=top_k
        )

        return {
            "question": question,
            "context": self.build_context(
                results
            ),
            "results": results,
            "sources": [
                {
                    "page": result["page"],
                    "section": result.get(
                        "section",
                        "Unknown section"
                    ),
                    "distance": result[
                        "distance"
                    ],
                    "text": result["text"]
                }
                for result in results
            ]
        }