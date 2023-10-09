from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    """"Return a freindly welcome message"""
    return  {'message': "Welcome to the Car Sharing service"}

