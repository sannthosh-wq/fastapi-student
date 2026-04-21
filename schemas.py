from pydantic import BaseModel

class Studentbase(BaseModel):
    Name : str
    Register_Number: int
    Result: str
    
class studentcreate(Studentbase):
    pass

class student(Studentbase):
    id : int
    class Config :
        from_attributes = True