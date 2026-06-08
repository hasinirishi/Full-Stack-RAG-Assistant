import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import chromadb

# Load environment variables from .env
load_dotenv()

# Create the FastAPI app
app = FastAPI(title="Document Q&A API")

# Allow the React frontend to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure LlamaIndex settings
Settings.llm = Gemini(model="models/gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
# Settings.embed_model = GeminiEmbedding(model_name="models/text-embedding-004", api_key=os.getenv("GEMINI_API_KEY"))
Settings.embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001", api_key=os.getenv("GEMINI_API_KEY"))

# Initialize ChromaDB
chroma_client = chromadb.Client()
chroma_collection = chroma_client.get_or_create_collection("documents")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Store the index globally
index = None

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global index

    # Only accept PDF files
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Save the uploaded file to disk
    file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
    content = await file.read()
    file_path.write_bytes(content)

    try:
        # Parse the PDF and split it into document chunks
        documents = SimpleDirectoryReader(input_files=[str(file_path)]).load_data()
        # Create a searchable vector index from the chunks
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
        return {"message": f"Successfully indexed {file.filename}", "pages": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    global index

    # Ensure a document has been uploaded first
    if index is None:
        raise HTTPException(status_code=400, detail="No document has been uploaded yet")

    # Create a query engine that retrieves the top 3 most relevant chunks
    query_engine = index.as_query_engine(similarity_top_k=3)
    response = query_engine.query(request.question)

    # Extract source text from the retrieved chunks
    sources = []
    for node in response.source_nodes:
        source_text = node.node.text[:200] + "..." if len(node.node.text) > 200 else node.node.text
        sources.append(source_text)

    return QueryResponse(answer=str(response), sources=sources)

 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
 
 