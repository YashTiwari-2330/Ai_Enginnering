from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
import json
import os

app = FastAPI(title="Student CRUD using JSON")

DATABASE = "database.json"


# ---------------------------
# Pydantic Model
# ---------------------------

class Student(BaseModel):
    id: Annotated[int, Field(gt=0, description="Enter Student ID")]
    name: Annotated[str, Field(min_length=2, max_length=20, description="Enter Student Name")]
    age: Annotated[int, Field(gt=0, le=100, description="Enter Student Age")]
    email: EmailStr


# ---------------------------
# Read Data
# ---------------------------

def read_data():
    if not os.path.exists(DATABASE):
        return {"students": []}

    try:
        with open(DATABASE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Database JSON is corrupted."
        )


# ---------------------------
# Write Data
# ---------------------------

def write_data(data):
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)


# ---------------------------
# GET ALL STUDENTS
# ---------------------------

@app.get("/students")
def get_students():

    data = read_data()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Students fetched successfully",
            "data": data["students"]
        }
    )


# ---------------------------
# GET STUDENT BY ID
# ---------------------------

@app.get("/students/{student_id}")
def get_student(student_id: int):

    data = read_data()

    for student in data["students"]:
        if student["id"] == student_id:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Student found",
                    "student": student
                }
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# ---------------------------
# CREATE STUDENT
# ---------------------------

@app.post("/students")
def create_student(student: Student):

    data = read_data()

    for std in data["students"]:
        if std["id"] == student.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student ID already exists"
            )

    data["students"].append(student.model_dump())

    write_data(data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Student created successfully",
            "student": student.model_dump()
        }
    )


# ---------------------------
# UPDATE STUDENT
# ---------------------------

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    data = read_data()

    for index, student in enumerate(data["students"]):

        if student["id"] == student_id:

            data["students"][index] = updated_student.model_dump()

            write_data(data)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Student updated successfully",
                    "student": updated_student.model_dump()
                }
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# ---------------------------
# DELETE STUDENT
# ---------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    data = read_data()

    for student in data["students"]:

        if student["id"] == student_id:

            data["students"].remove(student)

            write_data(data)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Student deleted successfully"
                }
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )