import os
import dotenv
from langchain_community.vectorstores import Chroma       # <-- CORRECTED import
from langchain_community.embeddings import HuggingFaceEmbeddings  # <-- CORRECTED import
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

# --- Load Environment Variables ---
dotenv.load_dotenv()
print("--- Starting Phase 3 (API Version) ---")

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if GROQ_API_KEY:
    print("GROQ_API_KEY loaded successfully.")
else:
    print("ERROR: Could not find 'GROQ_API_KEY' in .env file.")
    # You can exit here if you want:
    # exit()

# --- 1. Load our existing database ---
DB_DIR = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

print("Loading persistent vector database...")
db = Chroma(
    persist_directory=DB_DIR, 
    embedding_function=embeddings
)

# --- 2. Create the Retriever ---
retriever = db.as_retriever(
    search_type="similarity_score_threshold",  # Use score threshold to ensure quality
    search_kwargs={
        "k": 8,  # Increased from 5 to get more context
        "score_threshold": 0.5  # Only return relevant chunks
    }
)
print("Retriever is ready.")

# --- 3. Load the LLM (via Groq API) ---
print("Connecting to Groq API with Llama 3...")
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",  # A powerful, fast model
    temperature=0.1
)
print("LLM is ready.")

# --- 4. Create the RAG Chain ---
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

print("--- RAG Chatbot is Ready! ---")

# --- 5. Run a test query ---
# try:
#     query = "What are the main attractions to see in Paris?"
#     print(f"\nQuery: {query}")
#     print("Thinking...")

#     result = qa_chain.invoke({"query": query})

#     print("\n--- Answer ---")
#     print(result['result'])

#     print("\n--- Sources Used ---")
#     for doc in result['source_documents']:
#         source_file = doc.metadata.get('source', 'Unknown').split(os.path.sep)[-1]
#         print(f"File: {source_file}")
#         print(f"Text: {doc.page_content[:250]}...\n")

# except Exception as e:
#     print(f"\nAn error occurred: {e}")
#     if "401" in str(e):
#         print("This is an Authentication Error. Check your GROQ_API_KEY in the .env file.")