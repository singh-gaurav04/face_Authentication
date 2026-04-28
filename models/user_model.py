from sqlalchemy import Column,String, Float,Integer
from sqlalchemy.dialects.postgresql import ARRAY
from db.database import engine
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    embedding = Column(ARRAY(Float))  




