🔐📚 RAG Chatbot with Role-Based Access Control (RBAC)
This project is a Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, featuring JWT-based authentication and role-based access control. It enables secure access to chatbot functionality based on user roles (e.g., User, Admin), integrates with vector databases (FAISS), and uses HuggingFace embeddings for contextual Q&A from documents.

🚀 Features
✅ User Registration and Login with secure password hashing

🔐 JWT Authentication & Authorization

🧑‍💻 Role-Based Access Control (RBAC) (User, Admin)

🧠 Contextual Q&A powered by RAG (using HuggingFace + FAISS)

📁 Local Embedding Storage with FAISS

🛠️ API Endpoints:

/register – Create a new user

/login – Get JWT token

/query – Public query endpoint

/chat – Authenticated chat endpoint (JWT required)

/admin-data – Admin-only access endpoint

📦 Modular Codebase: main.py, auth.py, models.py, database.py, rag.py

🧱 Tech Stack
Backend: FastAPI

Auth: OAuth2 + JWT (via fastapi.security)

Database: SQLite + SQLAlchemy

Embedding: HuggingFace Transformers (all-MiniLM-L6-v2)

Vector DB: FAISS (local storage)

ML Backend: LangChain Q&A chain

Security: Passlib (bcrypt hashing), JWTBearer

Docs/Testing: Swagger UI (http://localhost:8000/docs)

📂 Project Structure
graphql
Copy
Edit
.
├── auth.py               # Authentication & JWT functions
├── database.py           # SQLAlchemy DB setup
├── models.py             # User model
├── main.py               # FastAPI routes and app
├── rag.py                # RAG Q&A logic with FAISS
├── faiss_index/          # Folder storing FAISS index and docs
├── requirements.txt
└── README.md
🛠️ Setup Instructions
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/rag-rbac-chatbot.git
cd rag-rbac-chatbot
Create virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up FAISS index and embeddings
Make sure you have your documents embedded and saved:

python
Copy
Edit
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_index", embeddings)
Run the server

bash
Copy
Edit
uvicorn main:app --reload
Test on Swagger UI
Visit: http://localhost:8000/docs

🔑 User Roles
Role	Access Level
User	Can access /chat, /query
Admin	Can access /chat, /query, /admin-data

✅ Example Usage
Register
json
Copy
Edit
POST /register
{
  "username": "jayant",
  "password": "securepass",
  "role": "admin"
}
Login
json
Copy
Edit
POST /login
Form Data:
username=jayant
password=securepass
→ Returns JWT token.

Chat Endpoint
http
Copy
Edit
GET /chat
Authorization: Bearer <your_token>
🔒 Security Practices
Passwords are hashed with bcrypt (via Passlib)

JWT token includes expiration

Role verification logic protects admin-only routes

No raw SQL – ORM used for safe DB operations

🌟 Future Enhancements
Upload documents via API

User-facing frontend (React/Vue)

Integration with cloud-based vector DB (e.g., Pinecone)

Logging, monitoring, and feedback loop support

🤝 Contributing
Contributions are welcome! Please open an issue or pull request if you'd like to collaborate.

📃 License
This project is licensed under the MIT License.
