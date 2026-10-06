from backend.rag.rag_service import RAGService
from backend.services.llm_service import LLMService


question = "Which software component is mentioned?"

rag = RAGService()
llm = LLMService()

result = rag.prepare_question(question, top_k=2)

answer = llm.generate_answer(
    question=result["question"],
    context=result["context"]
)

print("\nQUESTION:")
print(question)

print("\nAI ANSWER:")
print(answer)

print("\nSOURCES:")
for source in result["sources"]:
    print(f"Page {source['page']}")