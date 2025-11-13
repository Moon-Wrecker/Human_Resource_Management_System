"""
FastAPI REST API for RAG Application
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import tempfile
import shutil

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RAG API",
    description="REST API for RAG (Retrieval-Augmented Generation) Application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG instance
rag_instance = None

# Pydantic models for request/response
class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"

class QuestionResponse(BaseModel):
    answer: str
    sources: List[str]
    session_id: str

class SetupRequest(BaseModel):
    document_path: str = "text.txt"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_k: int = 3
    force_recreate: bool = False

class StatusResponse(BaseModel):
    status: str
    message: str

class SearchRequest(BaseModel):
    query: str
    k: int = 3

class SearchResponse(BaseModel):
    results: List[dict]


class AdvancedRAGApplication:
    """RAG Application class"""
    
    def __init__(self, document_path, persist_directory="./faiss_index"):
        self.document_path = document_path
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.chain = None
        self.chat_histories = {}  # Store multiple session histories
        
        # Initialize Google Gemini components
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
        )
    
    def load_and_process_document(self, chunk_size=1000, chunk_overlap=200):
        """Load the document and split it into chunks"""
        loader = TextLoader(self.document_path, encoding='utf-8')
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        return chunks
    
    def create_vectorstore(self, chunks):
        """Create FAISS vectorstore from document chunks"""
        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
    
    def save_vectorstore(self):
        """Save the FAISS index to disk"""
        if self.vectorstore:
            self.vectorstore.save_local(self.persist_directory)
    
    def load_vectorstore(self):
        """Load existing FAISS index from disk"""
        try:
            self.vectorstore = FAISS.load_local(
                self.persist_directory,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        except Exception as e:
            return False
    
    def setup_conversational_chain(self, k=3):
        """Set up the conversational retrieval chain with history"""
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, contextualize_q_prompt
        )
        
        qa_system_prompt = (
            "You are a helpful AI assistant. Use the following pieces of context to answer the question. "
            "If you don't know the answer based on the context provided, just say that you don't know, "
            "don't try to make up an answer. Keep your answer concise but informative.\n\n"
            "Context: {context}"
        )
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        self.chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    def get_chat_history(self, session_id: str):
        """Get chat history for a session"""
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = []
        return self.chat_histories[session_id]
    
    def ask(self, question: str, session_id: str = "default"):
        """Ask a question and get an answer with conversation context"""
        if not self.chain:
            raise ValueError("Chain not initialized. Run setup() first.")
        
        chat_history = self.get_chat_history(session_id)
        
        response = self.chain.invoke({
            "input": question,
            "chat_history": chat_history
        })
        
        # Update chat history
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=response["answer"]))
        
        return response
    
    def similarity_search(self, query, k=3):
        """Perform similarity search without LLM generation"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized.")
        
        docs = self.vectorstore.similarity_search(query, k=k)
        return docs
    
    def clear_memory(self, session_id: str = "default"):
        """Clear conversation memory for a session"""
        if session_id in self.chat_histories:
            self.chat_histories[session_id] = []
    
    def setup(self, force_recreate=False, chunk_size=1000, chunk_overlap=200, retrieval_k=3):
        """Complete setup of the RAG system"""
        if not force_recreate and self.load_vectorstore():
            pass  # Vector store loaded
        else:
            chunks = self.load_and_process_document(chunk_size, chunk_overlap)
            self.create_vectorstore(chunks)
            self.save_vectorstore()
        
        self.setup_conversational_chain(k=retrieval_k)


# API Endpoints

@app.on_event("startup")
async def startup_event():
    """Initialize RAG on startup"""
    global rag_instance
    try:
        rag_instance = AdvancedRAGApplication(
            document_path="text.txt",
            persist_directory="./faiss_index"
        )
        rag_instance.setup(force_recreate=False)
        print("✅ RAG Application initialized successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize RAG on startup: {e}")
        print("Please call /setup endpoint to initialize")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG API is running",
        "version": "1.0.0",
        "endpoints": {
            "POST /ask": "Ask a question",
            "POST /search": "Similarity search",
            "POST /setup": "Setup/reload RAG system",
            "POST /clear": "Clear conversation history",
            "GET /health": "Health check",
            "POST /upload": "Upload new document"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if rag_instance and rag_instance.chain:
        return {"status": "healthy", "rag_initialized": True}
    return {"status": "unhealthy", "rag_initialized": False}


@app.post("/setup", response_model=StatusResponse)
async def setup_rag(request: SetupRequest):
    """Setup or reload the RAG system"""
    global rag_instance
    
    try:
        rag_instance = AdvancedRAGApplication(
            document_path=request.document_path,
            persist_directory="./faiss_index"
        )
        
        rag_instance.setup(
            force_recreate=request.force_recreate,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
            retrieval_k=request.retrieval_k
        )
        
        return StatusResponse(
            status="success",
            message="RAG system setup successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question to the RAG system"""
    if not rag_instance or not rag_instance.chain:
        raise HTTPException(
            status_code=400,
            detail="RAG system not initialized. Please call /setup first."
        )
    
    try:
        result = rag_instance.ask(request.question, request.session_id)
        
        # Extract source content
        sources = [doc.page_content[:200] + "..." for doc in result.get('context', [])]
        
        return QuestionResponse(
            answer=result['answer'],
            sources=sources,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Perform similarity search in documents"""
    if not rag_instance or not rag_instance.vectorstore:
        raise HTTPException(
            status_code=400,
            detail="RAG system not initialized. Please call /setup first."
        )
    
    try:
        docs = rag_instance.similarity_search(request.query, request.k)
        
        results = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]
        
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear")
async def clear_history(session_id: str = "default"):
    """Clear conversation history for a session"""
    if not rag_instance:
        raise HTTPException(
            status_code=400,
            detail="RAG system not initialized."
        )
    
    try:
        rag_instance.clear_memory(session_id)
        return StatusResponse(
            status="success",
            message=f"Conversation history cleared for session: {session_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new document to replace the current one"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Copy to text.txt
        shutil.copy(tmp_path, "text.txt")
        os.unlink(tmp_path)
        
        # Reinitialize RAG with new document
        global rag_instance
        rag_instance = AdvancedRAGApplication(
            document_path="text.txt",
            persist_directory="./faiss_index"
        )
        rag_instance.setup(force_recreate=True)
        
        return StatusResponse(
            status="success",
            message=f"Document '{file.filename}' uploaded and RAG system reinitialized"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
