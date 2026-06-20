from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()

# Lode the file and data
def load_data():
    file_path = Path(__file__).with_name("patients.json")
    with open(file_path , 'r') as f:
        data = json.load(f)
    return data

# Home page        
@app.get("/")
def welcome():
    return {
        "message" : "Welcome to the PATIEENT MANAGEMENT SYSTEM."
    }

#About Page
@app.get("/about")
def about():
    return {
        "message" : "This is a patient management system Which use in Hospital to store and manage a details of the patients."
    }

#Patients List
@app.get("/patients")
def show_patients():
    data = load_data()
    return "Patients List : " + str(data)

@app.get('/patients/{patient_id}')
def show_patient(patient_id : str):
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient

    return "Patient not found."
    
