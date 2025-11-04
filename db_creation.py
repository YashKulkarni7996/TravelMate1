import time
import os
from math import ceil

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

try:
    import magic  # noqa: F401
    _HAS_MAGIC = True
except Exception:
    _HAS_MAGIC = False

# 1. Define paths and model
KNOWLEDGE_BASE_DIR = "KNOWLEDGE_BASE"
DB_DIR = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

print("--- Starting Phase 2: Building Vector Database ---")

if not _HAS_MAGIC:
    print("libmagic is unavailable; installing `python-magic-bin` (Windows) or `libmagic` is recommended for better filetype detection.")

if not os.path.isdir(KNOWLEDGE_BASE_DIR):
    raise FileNotFoundError(f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")

# 2. LOAD Documents
print(f"Loading .txt documents from {KNOWLEDGE_BASE_DIR} (this may take a little while)...")
start_time = time.time()
# Force TextLoader for .txt files to avoid optional heavy/unstructured dependencies
loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
documents = loader.load()
end_time = time.time()
print(f"Loaded {len(documents)} documents in {end_time - start_time:.2f} seconds.")

# 3. CHUNK Documents
print("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    # More focused chunk size that balances context vs. specificity
    chunk_size=1000,
    chunk_overlap=200,
    separators=[
        "\n==",     # Wiki major sections
        "\n===",    # Wiki subsections
        "\n====",   # Wiki sub-subsections
        "\n\n",     # Paragraphs
        "\n",       # Lines
        ". ",       # Sentences
        " ",        # Words
        ""          # Characters
    ]
)
chunks = text_splitter.split_documents(documents)
print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

# 4. EMBED and STORE (batched)
print("Loading embedding model and creating/persisting database in batches...")
print(f"Embedding model: {EMBEDDING_MODEL}")
start_time = time.time()

# Initialize the embedding model and persistent Chroma DB
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# Process in batches to reduce memory spikes
BATCH_SIZE = 512  # tune this based on available RAM/VRAM
total = len(chunks)
if total == 0:
    print("No chunks to embed. Exiting.")
else:
    batches = ceil(total / BATCH_SIZE)
    for i in range(batches):
        start = i * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch = chunks[start:end]
        print(f"Embedding batch {i+1}/{batches} (chunks {start}:{end})...")
        db.add_documents(batch)
        # Optionally persist after each batch
        db.persist()

end_time = time.time()
print("--- Vector Database Created Successfully! ---")
print(f"Total time: {end_time - start_time:.2f} seconds.")
print(f"Database saved to: {DB_DIR}")