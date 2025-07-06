from fastapi import FastAPI

app = FastAPI(title="File Service")

@app.get("/")
def read_root():
    return {"message": "File Service is running"}
