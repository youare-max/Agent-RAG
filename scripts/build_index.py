import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retriever import RAGRetriever

def main():
    print("开始构建向量索引...")
    retriever = RAGRetriever()
    print("向量索引构建完成！")

if __name__ == "__main__":
    main()
