import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retriever import RAGRetriever

def test_retrieve():
    retriever = RAGRetriever()
    results = retriever.retrieve("如何找回密码")
    assert len(results) > 0
    print("RAG检索测试通过")

if __name__ == "__main__":
    test_retrieve()
