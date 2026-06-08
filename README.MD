# 📄 Full-Stack PDF Q&A Assistant (RAG)

An intelligent, full-stack Document Q&A Assistant built with **React**, **FastAPI**, **LlamaIndex**, and **ChromaDB**. This application implements a full **RAG (Retrieval-Augmented Generation)** pipeline. Users can drag and drop a PDF file, which is automatically parsed, vectorized, and indexed. They can then chat with the document in real-time, receiving grounded, cited answers backed by Google's **Gemini 2.5 Flash** model.

---

## 🚀 Tech Stack

### Frontend
- **React (Vite)** - Modern, fast SPA framework
- **Axios** - HTTP client for backend API communication
- **CSS3** - Customized responsive interface with a drag-and-drop landing zone and clean chat window

### Backend
- **FastAPI** - High-performance Python web framework with asynchronous support
- **LlamaIndex** - Complete LLM data framework for document ingestion, chunking, and querying
- **ChromaDB** - High-performance in-memory vector database
- **Gemini API** - Powered by `models/gemini-2.5-flash` (for generation) and `models/gemini-embedding-001` (for embedding generation)
- **Uvicorn** - Lightning-fast ASGI server implementation

---

## 🛠️ Key Features
- **Drag-and-Drop Ingestion:** Clean user interface to upload PDF files directly.
- **On-the-Fly Indexing:** PDFs are parsed via LlamaIndex, converted into 768-dimensional vector embeddings, and stored dynamically inside a local ChromaDB collection.
- **Semantic Retrieval:** When a question is asked, the system retrieves the top 3 most semantically similar context chunks.
- **Answer Grounding with Sources:** The assistant generates answers based *only* on the document context and renders the source chunks directly on-screen to prevent hallucination.
- **Windows Optimized Setup:** Fully configured for PowerShell script policies and C++ native compiler requirements.

---

## ⚙️ Installation & Setup (Windows Guide)

### 1. Backend Setup
Clone the repository and navigate to the backend folder:
```bash
cd doc-qa-assistant/backend
```

Create and activate a Python virtual environment:
```powershell
# If using Windows PowerShell, enable script execution first:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Build and activate
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Note:** Building `chroma-hnswlib` on Windows requires the **Microsoft Visual C++ Build Tools** (specifically the "Desktop development with C++" workload) to compile native C++ components.

Install backend dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Start the FastAPI server:
```bash
python -m uvicorn main:app --reload
```
Verify the backend is live at [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health).

---

### 2. Frontend Setup
In a new terminal window, navigate to the frontend folder:
```bash
cd doc-qa-assistant/frontend
```

Install packages and start the Vite dev server:
```bash
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser to view the application!

---

## 🧠 How the RAG Pipeline Works
1. **Document Loading:** The PDF is uploaded and parsed into raw text using LlamaIndex's `SimpleDirectoryReader`.
2. **Chunking & Embedding:** The text is split into distinct nodes. Each node is vectorized using Google's `gemini-embedding-001` model.
3. **Vector Storage:** The vectors and text nodes are stored inside a local `ChromaVectorStore` collection.
4. **Query & Context Matching:** When the user enters a question, it is vectorized and compared against the store using semantic search to find the 3 most relevant nodes.
5. **Grounded Generation:** The nodes are fed to the `gemini-2.5-flash` model alongside the user query to synthesize a cited response.

---

## 🤝 Acknowledgments
- NextWork Platform for the backend/frontend scaffolding framework guidance.
- Google AI Studio for providing free tier access to Gemini Embeddings and LLM endpoints.