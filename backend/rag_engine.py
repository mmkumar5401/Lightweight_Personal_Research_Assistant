from pathlib import Path
import re, unicodedata
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

DATA_DIR = Path(__file__).parent / "data"
PAPERS_DIR = DATA_DIR / "papers"
VECTOR_DIR = DATA_DIR / "vector_store"

def load_documents(path=PAPERS_DIR):
    docs = []
    for file in Path(path).glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        docs.extend(loader.load())
    print(f"Loaded {len(docs)} documents from {path}")
    return docs


def super_clean(text):
    if not isinstance(text, str):
        try:
            text = text.decode("utf-8", errors="ignore")
        except Exception:
            text = str(text)
    
    text = unicodedata.normalize("NFKD", text) # Normalize any weird Unicode (e.g. accented letters, subscripts)
    text = re.sub(r"[\x00-\x1F\x7F-\x9F]", " ", text) # Remove all control / non-printable characters
    text = re.sub(r"[^ -~\s]", " ", text) # Replace everything that isn’t “normal printable” or whitespace
    text = re.sub(r"\s+", " ", text).strip() # Collapse spaces and trim
    return text if text else None

def create_vector_store(docs, persist_dir=VECTOR_DIR):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # Clean every chunk
    raw_texts = []
    for c in chunks:
        cleaned = super_clean(getattr(c, "page_content", ""))
        if cleaned:
            raw_texts.append(cleaned)

    print(f"Embedding {len(raw_texts)} sanitized chunks...")

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Final safety net: skip any chunk that still breaks encode()
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")

    safe_texts = []
    for i, t in enumerate(raw_texts):
        try:
            model.encode([t])
            safe_texts.append(t)
        except Exception as e:
            print(f"⚠️  Skipping chunk {i} ({len(t)} chars): {e}")

    print(f"✅ {len(safe_texts)} safe chunks out of {len(raw_texts)} total")

    vectordb = Chroma.from_texts(
        texts=safe_texts,
        embedding=embedder,
        persist_directory=str(persist_dir),
    )
    vectordb.persist()
    print("✅ Vector store created successfully.")
    return vectordb

def get_qa_chain():
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=str(VECTOR_DIR), embedding_function=embedder)
    retriever = vectordb.as_retriever(search_kwargs={"k": 8})
    llm = Ollama(model="mistral")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa
