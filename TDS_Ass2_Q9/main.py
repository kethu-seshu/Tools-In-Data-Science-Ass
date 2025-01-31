from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS for GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Read CSV file into memory
def load_students():
    students = []
    with open("q-fastapi.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append({"studentId": int(row["studentId"]), "class": row["class"]})
    return students

students_data = load_students()

@app.get("/api")
def get_students(class_: list[str] = Query(None, alias="class")):
    if class_:
        filtered_students = [s for s in students_data if s["class"] in class_]
        return {"students": filtered_students}
    return {"students": students_data}

