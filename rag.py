import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub

# Load environment variables
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Load HuggingFace sentence embeddings (no token needed here)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load or create the FAISS vectorstore
if os.path.exists("faiss_index/index.faiss"):
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
else:
    from langchain_community.document_loaders import TextLoader
    from langchain.text_splitter import CharacterTextSplitter

    loader = TextLoader("sample.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(documents)

    db = FAISS.from_documents(documents, embeddings)
    db.save_local("faiss_index")

# Initialize the LLM (token is needed here)
llm = HuggingFaceHub(
    repo_id="google/flan-t5-base",
    huggingfacehub_api_token=hf_token,
    model_kwargs={"temperature": 0.5, "max_length": 256}
)

# Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever()
)

# Main query-answering function
def answer_query(query: str):
    return qa_chain.run(query)
