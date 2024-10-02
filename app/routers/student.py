from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.student_service import get_student_by_id, create_student, update_student, delete_student, get_students
from app.schemas.student import Student, StudentCreate
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Student)
def create_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db=db, student=student)

@router.get("/", response_model=list[Student])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_students(db, skip=skip, limit=limit)

@router.get("/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.patch("/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    updated_student = update_student(db, student_id=student_id, student=student)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = delete_student(db, student_id=student_id)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}
