import os
import dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

dotenv.load_dotenv()
print("--- Starting Curated Paris RAG (PoC) ---")

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found; set it in .env to use the LLM.")

DB_DIR = "chroma_db_paris_curated"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model (curated)...")
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

print("Loading curated persistent vector database...")
db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k":6, "score_threshold":0.35})
print("Retriever is ready (curated DB).")

print("Connecting to Groq API with Llama 3... (curated PoC)")
llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.1)
print("LLM is ready.")

qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

print("--- Curated Paris RAG Chatbot (PoC) is Ready! ---")
