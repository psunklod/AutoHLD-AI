import time
from backend.rag.rag_service import RAGService
from backend.services.llm_service import LLMService

question = "What are the dependencies between the software components?"

start = time.perf_counter()

rag = RAGService()
result = rag.prepare_question(question, top_k=3)

llm = LLMService()
answer = llm.generate_answer(
    question=result["question"],
    context=result["context"]
)

elapsed = time.perf_counter() - start

print("\n" + "="*60)
print("AUTOHLD AI EVALUATION - RAG DEPENDENCY TEST")
print("="*60)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)

print("\nSOURCES:")
for source in result.get("sources", []):
    print(
        f"Page: {source.get('page')} | "
        f"Section: {source.get('section')} | "
        f"Distance: {source.get('distance')}"
    )

print(f"\nLATENCY: {elapsed:.2f} seconds")
print("="*60)
