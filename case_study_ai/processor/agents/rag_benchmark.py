from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from .utils import get_llm

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.load_local(
    "rag_benchmark_index",
    embeddings=embedding,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever()

rag_benchmark_agent = RetrievalQA.from_chain_type(
    llm=get_llm(),
    retriever=retriever,
    chain_type="stuff"
)
