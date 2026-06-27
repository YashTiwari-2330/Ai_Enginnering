from fastapi import FastAPI , Path , HTTPException, Query
import json
from pathlib import Path as FilePath

app = FastAPI()

# Lode the file and data
def load_data():
    file_path = FilePath(__file__).with_name("patients.json")
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
def show_patient(patient_id : str = Path(..., description="The ID of the patient to retrieve" , example = "P001")):
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(status_code=404 , detail=f"Patient With ID {patient_id} not found..")
    
# Sort data
@app.get('/sort')
def sort_patients(sort_by : str = Query(..., description="The field to sort the patients basis of hight , weight or bmi"), order : str = Query('asc' , description="Sort in asc and dasc order")):

    valid_fields = ["height" , "weight" , "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 , detail=f"Enter a valid field from {valid_fields}")
    
    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code=400 , detail= f"Enter a valid order from ['asc'] or ['desc'] ")
    
    data = load_data()

    sorted_data = sorted(data, key = lambda x : x.get(sort_by) , reverse = (order == 'desc'))

    return sorted_data
    

