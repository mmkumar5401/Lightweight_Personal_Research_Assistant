from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag_engine import load_documents, create_vector_store, get_qa_chain
import threading

app = FastAPI()
qa_chain = None
init_done = False

class Query(BaseModel):
    question: str

def init_vector_store():
    global qa_chain, init_done
    docs = load_documents()
    create_vector_store(docs)
    qa_chain = get_qa_chain()
    init_done = True
    print("System initialized.")

@app.on_event("startup")
def startup_event():
    threading.Thread(target=init_vector_store, daemon=True).start()

@app.post("/ask")
def ask(query: Query):
    global qa_chain, init_done
    if not init_done:
        return {"answer": "System still initializing. Try again in a few seconds."}
    response = qa_chain.run(query.question)
    return {"answer": response}
