import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

class AdvancedRAGApplication:
    def __init__(self, document_path, persist_directory="./faiss_index"):
        """
        Initialize the Advanced RAG application with conversation memory
        
        Args:
            document_path: Path to the text document
            persist_directory: Directory to save/load FAISS index
        """
        self.document_path = document_path
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.chain = None
        self.chat_history = []
        
        # Initialize Google Gemini components
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
        )
    
    def load_and_process_document(self, chunk_size=1000, chunk_overlap=200):
        """
        Load the document and split it into chunks
        
        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
        """
        print("Loading document...")
        
        # Load the text file
        loader = TextLoader(self.document_path, encoding='utf-8')
        documents = loader.load()
        
        print(f"Loaded {len(documents)} document(s)")
        print(f"Total characters: {sum(len(doc.page_content) for doc in documents)}")
        
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        
        return chunks
    
    def create_vectorstore(self, chunks):
        """Create FAISS vectorstore from document chunks"""
        print("Creating embeddings and vector store...")
        print("This may take a while depending on the document size...")
        
        # Create FAISS vectorstore
        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        print("✅ Vector store created successfully!")
        
    def save_vectorstore(self):
        """Save the FAISS index to disk"""
        if self.vectorstore:
            self.vectorstore.save_local(self.persist_directory)
            print(f"💾 Vector store saved to {self.persist_directory}")
    
    def load_vectorstore(self):
        """Load existing FAISS index from disk"""
        try:
            self.vectorstore = FAISS.load_local(
                self.persist_directory,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"✅ Vector store loaded from {self.persist_directory}")
            return True
        except Exception as e:
            print(f"⚠️  Could not load vector store: {e}")
            return False
    
    def setup_conversational_chain(self, k=3):
        """
        Set up the conversational retrieval chain with history
        
        Args:
            k: Number of relevant chunks to retrieve
        """
        
        # Create retriever
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        
        # Contextualize question prompt
        # This system prompt helps the AI reformulate the question based on chat history
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
        
        # Create question-answer chain
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        
        # Create the full RAG chain
        self.chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        
        print(f"✅ Conversational chain set up! (Retrieving top {k} chunks)")
    
    def ask(self, question):
        """
        Ask a question and get an answer with conversation context
        
        Args:
            question: The question to ask
            
        Returns:
            dict: Contains 'answer' and 'context' (source documents)
        """
        if not self.chain:
            raise ValueError("Chain not initialized. Run setup() first.")
        
        # Invoke the chain with chat history
        response = self.chain.invoke({
            "input": question,
            "chat_history": self.chat_history
        })
        
        # Update chat history
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=response["answer"]))
        
        return response
    
    def similarity_search(self, query, k=3):
        """
        Perform similarity search without LLM generation
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized.")
        
        docs = self.vectorstore.similarity_search(query, k=k)
        return docs
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.chat_history = []
        print("🧹 Conversation memory cleared!")
    
    def setup(self, force_recreate=False, chunk_size=1000, chunk_overlap=200, retrieval_k=3):
        """
        Complete setup of the RAG system
        
        Args:
            force_recreate: If True, recreate the vector store even if it exists
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            retrieval_k: Number of chunks to retrieve for answering
        """
        print("\n" + "="*60)
        print("🚀 Setting up Advanced RAG Application")
        print("="*60 + "\n")
        
        # Try to load existing vectorstore
        if not force_recreate and self.load_vectorstore():
            print("📂 Using existing vector store")
        else:
            # Load and process document
            chunks = self.load_and_process_document(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
            # Create vectorstore
            self.create_vectorstore(chunks)
            
            # Save vectorstore
            self.save_vectorstore()
        
        # Setup chain
        self.setup_conversational_chain(k=retrieval_k)
        
        print("\n" + "="*60)
        print("✅ RAG Application Ready!")
        print("="*60 + "\n")


def print_sources(source_documents):
    """Pretty print source documents"""
    print(f"\n{'='*60}")
    print(f"📚 Retrieved {len(source_documents)} relevant sources:")
    print(f"{'='*60}")
    
    for i, doc in enumerate(source_documents, 1):
        print(f"\n📄 Source {i}:")
        print("-" * 60)
        content = doc.page_content.strip()
        # Show first 300 characters
        if len(content) > 300:
            print(content[:300] + "...")
        else:
            print(content)


def main():
    """Main function to demonstrate the Advanced RAG application"""
    
    # Initialize the RAG application
    rag = AdvancedRAGApplication(
        document_path="text.txt",
        persist_directory="./faiss_index"
    )
    
    # Setup the system
    rag.setup(
        force_recreate=False,  # Set to True to rebuild index
        chunk_size=1000,
        chunk_overlap=200,
        retrieval_k=3
    )
    
    # Interactive query loop
    print("💬 Chat with your documents!")
    print("Commands:")
    print("  - Type your question to get an answer")
    print("  - 'clear' to clear conversation history")
    print("  - 'search: <query>' to perform similarity search")
    print("  - 'quit' or 'exit' to stop")
    print("\n" + "="*60 + "\n")
    
    while True:
        user_input = input("🤔 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == 'clear':
            rag.clear_memory()
            continue
        
        if user_input.lower().startswith('search:'):
            query = user_input[7:].strip()
            try:
                docs = rag.similarity_search(query, k=3)
                print_sources(docs)
            except Exception as e:
                print(f"\n❌ Error: {e}")
            continue
        
        try:
            # Get answer
            print("\n🤖 Assistant: ", end="", flush=True)
            result = rag.ask(user_input)
            
            # Print answer
            print(result['answer'])
            
            # Optionally show sources (uncomment to enable)
            # print_sources(result['context'])
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        print()  # Empty line for readability


if __name__ == "__main__":
    main()
