from pydantic import BaseModel , EmailStr , Field , field_validator , model_validator , computed_field
from typing import List , Dict , Tuple , Optional , Annotated

class Patient(BaseModel):

    name : str
    age : Annotated[int , Field(gt=18 , title="Age" , discription="Age above the 18 " , example=[18,19] , strict=True)]
    email : EmailStr
    weight : float
    height : float
    dob : Tuple[int , int , int]
    sex : str
    admission : Tuple[int , int , int]
    allergies : Optional[List[str]] = None
    contacts  :  Dict[str , str]

    @field_validator('email')
    @classmethod
    def email_validator(cls , value):
        valid_domain = ["hdfc.com" , "icic.com" , "kotak.com"]

        domain_name = value.split("@")[-1]

        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        
        return value
    
    # Apply validation on name
    @field_validator('name')
    @classmethod

    def validation(cls , value):
        return value.upper()
    

    # If age is above 51 emegency contact compalsary
    @model_validator(mode="after")
    def validate_emergency(cls , model):
        if model.age > 50 and 'emergency' not in model.contacts:
            raise ValueError("Patients older than 50 so emergency contacts are complasary ")
        return model
    
    @computed_field()
    @property
    def caluclate_bmi(self) -> float :
        bmi = round((self.weight / self.height**2),2)
        return bmi



def insert_patient(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.height)
    print(patient.dob)
    print(patient.sex)
    print(patient.admission)
    print(patient.allergies)
    print(patient.contacts)
    print(patient.caluclate_bmi)
    print("Inserted data")

patient_info = {
    "name"  : "Yash",
    "age"   :  58,
    "email" : "yashtiwari2330@icic.com",
    "weight": 70.2,
    "height" : 6.4,
    "dob"   : (2 , 12 , 2000),
    "sex"   : "male", 
    "admission": (30 , 11 , 2000),
    "contacts" : {
        "home" : "000-555-888",
        "emergency":"9825887412"
    }
} 

patient1 = Patient(**patient_info)
insert_patient(patient1)
