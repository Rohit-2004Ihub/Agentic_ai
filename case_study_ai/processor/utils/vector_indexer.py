import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

# ✅ Load API key from .env
load_dotenv()

# ✅ Initialize embeddings globally or inside the function
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ✅ PDF text extractor
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ✅ FAISS builder function
def build_faiss_index(doc_folder="rag_data/"):
    all_docs = []

    for file in os.listdir(doc_folder):
        if file.endswith(".pdf"):
            path = os.path.join(doc_folder, file)
            content = extract_text_from_pdf(path)
            all_docs.append(Document(page_content=content))

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)

    # ✅ Use previously initialized `embedding`
    vectorstore = FAISS.from_documents(chunks, embedding)
    vectorstore.save_local("rag_benchmark_index")
