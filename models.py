from sqlalchemy import Column,String,Integer
from database import Base

class Student(Base):
    __tablename__ = "Student"
    
    id = Column(Integer,primary_key=True,index=True)
    Name = Column(String,nullable=False)
    Register_Number = Column(Integer,unique=True,nullable=False)
    Result = Column(String,nullable=False)