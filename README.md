# Ai_Enginnering
Step by step and phase by phase understand and learning to become a Ai Enginer

# Phase 0

# Start With Fundamental of Python
-> Variable , datatype, loops , conditional statemnt,oops etc...

# Second i cover version control..
-> Learn about git , github , branches , merge branch , conflic merge branch , 
    Slash , git tags , diff , rebase

# Phase 1

# Start FastAPI Fundamental

## Topics
- FastAPI
- Pydantic (data validation)

# Start FastAPI Fudamental


-> 1- Installtion Fast api.

1) Create virtual env (optional)
-> source .venv/bin/activate

2) Install FastAPI + Uvicorn
-> pip install fastapi uvicorn


========================================
6) About HTTP Methods?
========================================
1. An HTTP Methods is a set of request methods used to
   perform CRUD operations on resources in a RESTful API.

   it's a way for clients to communicate with servers.

In this project (Patient Management System) you are using:
- GET: to fetch data (Home / About / Patients / Single Patient)


========================================
6) About Path and Query Parameters?
========================================
-> Path Parameters:
- Used to identify a specific resource in the URL path.
- Example:- Check specific patients using url:
            localhost:8000/patients/P002 -> fetch patient with id = P002


========================================
7) About Page (Patient Management)
========================================
This is a patient management system Which use in Hospital to store and manage a details of the patients.

Routes in this project:
- / -> Home page
- /about -> About Page
- /patients -> Patients List
- /patients/{patient_id} -> Get specific patient by id


