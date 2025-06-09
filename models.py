from sqlalchemy import Column, Integer, String, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"
    auditor = "auditor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(RoleEnum))
