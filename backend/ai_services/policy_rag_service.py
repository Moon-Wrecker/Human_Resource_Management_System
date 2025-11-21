"""
Policy RAG Service - AI-powered policy question answering
Auto-indexes policies when uploaded via Policies API
"""
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Check if required libraries are available
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain_community.document_loaders import TextLoader, PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain.chains import create_retrieval_chain, create_history_aware_retriever
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from config import settings

logger = logging.getLogger("policy_rag_service")


class PolicyRAGService:
    """
    Policy RAG (Retrieval-Augmented Generation) Service
    
    Provides AI-powered question answering about company policies
    Auto-indexes policies when they are uploaded
    """
    
    def __init__(self):
        """Initialize the Policy RAG service"""
        if not LANGCHAIN_AVAILABLE:
            logger.error("LangChain libraries not installed. Install with: pip install -r requirements_ai.txt")
            raise ImportError("LangChain libraries required for Policy RAG service")
        
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not set in environment variables")
            raise ValueError("GOOGLE_API_KEY is required for Policy RAG service")
        
        self.api_key = settings.GOOGLE_API_KEY
        self.index_dir = settings.POLICY_RAG_INDEX_DIR
        self.vectorstore = None
        self.chain = None
        
        # Initialize components
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=settings.GEMINI_EMBEDDING_MODEL,
                google_api_key=self.api_key
            )
            
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                temperature=settings.GEMINI_TEMPERATURE,
                google_api_key=self.api_key
            )
            
            logger.info("Policy RAG Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Policy RAG Service: {e}")
            raise
    
    def load_index(self) -> bool:
        """
        Load existing FAISS index from disk
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            if os.path.exists(self.index_dir) and os.path.isdir(self.index_dir):
                self.vectorstore = FAISS.load_local(
                    self.index_dir,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self._setup_chain()
                logger.info(f"Loaded existing policy index from {self.index_dir}")
                return True
            else:
                logger.info("No existing policy index found")
                return False
        except Exception as e:
            logger.error(f"Error loading policy index: {e}")
            return False
    
    def index_policy_document(self, file_path: str, policy_title: str = "") -> bool:
        """
        Index a single policy document
        
        Args:
            file_path: Path to the policy PDF file
            policy_title: Title of the policy (for metadata)
            
        Returns:
            bool: True if indexed successfully
        """
        try:
            logger.info(f"Indexing policy document: {file_path}")
            
            # Load document
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding='utf-8')
            
            documents = loader.load()
            
            # Add metadata
            for doc in documents:
                doc.metadata["policy_title"] = policy_title or Path(file_path).stem
                doc.metadata["source"] = file_path
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.POLICY_RAG_CHUNK_SIZE,
                chunk_overlap=settings.POLICY_RAG_CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = text_splitter.split_documents(documents)
            logger.info(f"Split policy into {len(chunks)} chunks")
            
            # Create or update vector store
            if self.vectorstore is None:
                # Create new vector store
                self.vectorstore = FAISS.from_documents(
                    documents=chunks,
                    embedding=self.embeddings
                )
                logger.info("Created new policy vector store")
            else:
                # Add to existing vector store
                self.vectorstore.add_documents(chunks)
                logger.info("Added policy to existing vector store")
            
            # Save to disk
            self.vectorstore.save_local(self.index_dir)
            logger.info(f"Saved policy index to {self.index_dir}")
            
            # Setup chain
            self._setup_chain()
            
            return True
            
        except Exception as e:
            logger.error(f"Error indexing policy document: {e}")
            return False
    
    def index_all_policies(self, policy_dir: str) -> Dict[str, Any]:
        """
        Index all policy documents in a directory
        
        Args:
            policy_dir: Directory containing policy PDF files
            
        Returns:
            dict: Summary of indexing operation
        """
        try:
            policy_dir = Path(policy_dir)
            if not policy_dir.exists():
                logger.error(f"Policy directory not found: {policy_dir}")
                return {"success": False, "error": "Directory not found"}
            
            policy_files = list(policy_dir.glob("*.pdf"))
            if not policy_files:
                logger.warning(f"No PDF files found in {policy_dir}")
                return {"success": True, "indexed": 0, "message": "No policies to index"}
            
            logger.info(f"Found {len(policy_files)} policy files to index")
            
            indexed = 0
            failed = []
            
            for policy_file in policy_files:
                try:
                    if self.index_policy_document(str(policy_file), policy_file.stem):
                        indexed += 1
                    else:
                        failed.append(policy_file.name)
                except Exception as e:
                    logger.error(f"Failed to index {policy_file.name}: {e}")
                    failed.append(policy_file.name)
            
            return {
                "success": True,
                "total": len(policy_files),
                "indexed": indexed,
                "failed": failed
            }
            
        except Exception as e:
            logger.error(f"Error in batch indexing: {e}")
            return {"success": False, "error": str(e)}
    
    def _setup_chain(self):
        """Setup the conversational RAG chain"""
        if self.vectorstore is None:
            logger.warning("Cannot setup chain: vector store not initialized")
            return
        
        try:
            # Create retriever
            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.POLICY_RAG_RETRIEVAL_K}
            )
            
            # Contextualize question prompt
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
            
            # Create history-aware retriever
            history_aware_retriever = create_history_aware_retriever(
                self.llm, retriever, contextualize_q_prompt
            )
            
            # Answer question prompt
            qa_system_prompt = (
                "You are a helpful HR assistant answering questions about company policies. "
                "Use the following pieces of policy documents to answer the question. "
                "If you don't know the answer based on the provided policies, say that you don't know. "
                "Be concise but informative. Always cite the specific policy when possible.\n\n"
                "Context: {context}"
            )
            
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            # Create question-answer chain
            question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
            
            # Create the full RAG chain
            self.chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
            
            logger.info("Policy RAG chain setup successfully")
            
        except Exception as e:
            logger.error(f"Error setting up RAG chain: {e}")
            raise
    
    def ask_question(self, question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Ask a question about policies
        
        Args:
            question: The question to ask
            chat_history: Previous chat messages (optional)
            
        Returns:
            dict: Contains 'answer' and 'sources'
        """
        if not self.chain:
            # Try to load index
            if not self.load_index():
                return {
                    "success": False,
                    "error": "No policies indexed yet. Please upload policies first."
                }
        
        try:
            # Convert chat history to LangChain format
            lc_chat_history = []
            if chat_history:
                for msg in chat_history:
                    if msg["role"] == "user":
                        lc_chat_history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        lc_chat_history.append(AIMessage(content=msg["content"]))
            
            # Invoke chain
            response = self.chain.invoke({
                "input": question,
                "chat_history": lc_chat_history
            })
            
            # Extract sources
            sources = []
            if "context" in response:
                for doc in response["context"]:
                    sources.append({
                        "policy_title": doc.metadata.get("policy_title", "Unknown"),
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                    })
            
            return {
                "success": True,
                "answer": response["answer"],
                "sources": sources,
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_suggestions(self) -> List[str]:
        """Get suggested questions based on indexed policies"""
        return [
            "How many casual leaves am I allowed per year?",
            "What is the policy for sick leave?",
            "How do I enroll in the health insurance plan?",
            "What are the work from home guidelines?",
            "What is the remote work policy?",
            "How do I apply for maternity/paternity leave?",
            "What expenses can I claim reimbursement for?",
            "What is the notice period for resignation?"
        ]
    
    def get_index_status(self) -> Dict[str, Any]:
        """Get status of the policy index"""
        try:
            if self.vectorstore is None:
                self.load_index()
            
            if self.vectorstore is None:
                return {
                    "indexed": False,
                    "total_documents": 0,
                    "message": "No policies indexed yet"
                }
            
            # Get index stats
            index_stats = self.vectorstore.index.ntotal if hasattr(self.vectorstore, 'index') else 0
            
            return {
                "indexed": True,
                "total_vectors": index_stats,
                "index_location": self.index_dir,
                "model": settings.GEMINI_MODEL,
                "embedding_model": settings.GEMINI_EMBEDDING_MODEL
            }
            
        except Exception as e:
            logger.error(f"Error getting index status: {e}")
            return {
                "indexed": False,
                "error": str(e)
            }

