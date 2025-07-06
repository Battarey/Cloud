from fastapi import FastAPI

app = FastAPI(title="Virus Scan Service")

@app.get("/")
def read_root():
    return {"message": "Virus Scan Service is running"}
