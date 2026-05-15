import os
import faiss
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from config.settings import settings

class RAGRetriever:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.vector_store = None
        self._load_or_build_index()
    
    def _load_or_build_index(self):
        if os.path.exists(settings.VECTOR_DB_PATH):
            self.vector_store = FAISS.load_local(
                settings.VECTOR_DB_PATH, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            self._build_index()
    
    def _build_index(self):
        loader = DirectoryLoader(
            settings.KNOWLEDGE_BASE_PATH,
            glob="**/*.md",
            loader_cls=TextLoader
        )
        documents = loader.load()
        
        text_splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separator="\n"
        )
        split_docs = text_splitter.split_documents(documents)
        
        self.vector_store = FAISS.from_documents(split_docs, self.embeddings)
        os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
        self.vector_store.save_local(settings.VECTOR_DB_PATH)
    
    def retrieve(self, query, k=3):
        if not self.vector_store:
            return []
        docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    
    def update_knowledge_base(self):
        self._build_index()
