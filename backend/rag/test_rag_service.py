from backend.rag.rag_service import RAGService


rag = RAGService()

question = "Which software component is mentioned?"

result = rag.prepare_question(question, top_k=2)

print("\nQUESTION:")
print(result["question"])

print("\nRETRIEVED CONTEXT:")
print(result["context"])

print("\nSOURCES:")
for source in result["sources"]:
    print(
        f"Page {source['page']} | "
        f"Distance {source['distance']:.4f}"
    )