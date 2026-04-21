from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from schemas import student as studentSchema,studentcreate
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import Student
Base.metadata.create_all(bind= engine)


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - Create student
@app.post("/students",response_model=studentSchema)
def create(student: studentcreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student )
    return db_student

# GET - one student
@app.get("/result/{register_number}")
def get_result(register_number: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.Register_Number == register_number
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

# PUT - Update student
@app.put("/student.update/{student_id}",response_model=studentSchema)
def Update_student(student_id:int, updated: studentcreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="student Not Found")
    for key, value in updated.dict().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

# DELETE - Delete student
@app.delete("/student.students/{student_id}")
def delete_student(student_id:int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="student Not Found")
    db.delete(student)
    db.commit()
    return{"message":"student deleted successfully"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
    
@app.get("/all")
def get_all(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students
    
