from pydantic import BaseModel
from rag import answer_query, qa_chain

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth import create_access_token, verify_token, hash_password, verify_password
from database import SessionLocal
from models import User, RoleEnum

app = FastAPI()

# ----------------------------
# Auth security scheme for Swagger
# ----------------------------
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            return credentials.credentials
        raise HTTPException(status_code=403, detail="Invalid authorization")

oauth2_scheme = JWTBearer()

# ----------------------------
# Request Models
# ----------------------------
class QueryRequest(BaseModel):
    query: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: RoleEnum = RoleEnum.user  # default role is user

# ----------------------------
# DB Session Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Register Endpoint
# ----------------------------
@app.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pwd = hash_password(request.password)
    new_user = User(username=request.username, password=hashed_pwd, role=request.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "username": new_user.username}

# ----------------------------
# Login Endpoint
# ----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}

# ----------------------------
# Get Current User from Token
# ----------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ----------------------------
# Admin-Only Endpoint
# ----------------------------
@app.get("/admin-data")
def admin_data(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"secret_data": "Only admins can see this"}

# ----------------------------
# Authenticated Query Endpoint
# ----------------------------
@app.post("/chat")
def chat_endpoint(request: QueryRequest, current_user: User = Depends(get_current_user)):
    query = request.query
    try:
        answer = qa_chain.run(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    return {"answer": answer}

# ----------------------------
# Public Unauthenticated Query Endpoint
# ----------------------------
@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        answer = answer_query(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    return {"response": answer}

