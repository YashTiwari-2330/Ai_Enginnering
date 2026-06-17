from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def hello():
    return {"message" : "Hello World"}

@app.get("/about")

def about():
    return {
        "name" : "Yash",
        "age" : 20,
        "Income" : 0
    }