from typing import Annotated, Literal, Optional
import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI , Query ,HTTPException
from pydantic import BaseModel, Field, computed_field 

app = FastAPI()


class Patients(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Enter Patient Name", min_length=2)]
    age: Annotated[int, Field(..., gt=0, description="Enter Your Age")]
    city: Annotated[str, Field(..., description="Enter City Name", min_length=2)]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="Gender of the patients")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="Enter Patient Height")]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="Enter Patient Weight")]

    @computed_field(return_type=float)
    @property
    def bmi(self) -> float:
        if self.height is None or self.weight is None:
            return 0.0
        return round(self.weight / (self.height ** 2), 2)

    @computed_field(return_type=str)
    @property
    def verdict(self):
        if self.bmi < 18.5:
            return "UnderWeight"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, strict=True, gt=0)]
    city: Annotated[Optional[str], Field(default=None, strict=True)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json" , "w") as f:
        json.dump(data, f, indent=2)

@app.get("/")
def hello():
    return {
        'message' : "Patient Management System Application"
    }

@app.get("/about")
def about():
    return {
        'message' : "This web application store a information about the patient , so it help doctor to understand the dignosis"
    }

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patients")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight and bmi"),
    order: str = Query("asc", description="Sort order: asc or desc"),
):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field selected. Choose from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")

    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient : Patients):

    #load existing data
    data = load_data()
    
    #check if patient alredy exist

    if patient.id in data:
        raise HTTPException(status_code=400 , detail="Patient alredy exist")
    
    #if new patient so add it in database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into json file
    save_data(data)

    return JSONResponse(status_code=201 , content={'message' : "Patient created successfully"})

@app.put('/edit/{patient_id}')
def update_patient(patient_id : str , patient_update : PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient Not Found")
    
    existing_patient = data[patient_id]

    updated_info = patient_update.model_dump(exclude_unset=True)
    existing_patient.update(updated_info)

    height = existing_patient.get("height")
    weight = existing_patient.get("weight")
    if height is not None and weight is not None:
        existing_patient["bmi"] = round(weight / (height ** 2), 2)
    else:
        existing_patient["bmi"] = 0.0

    if existing_patient["bmi"] < 18.5:
        existing_patient["verdict"] = "UnderWeight"
    elif existing_patient["bmi"] < 30:
        existing_patient["verdict"] = "Normal"
    else:
        existing_patient["verdict"] = "Obese"

    data[patient_id] = existing_patient

    # Save data
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "patient updated"})

@app.delete('/delete{patient_id}')
def delete_patient(patient_id:str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200 , content="Patient Deleted Successfully..")
