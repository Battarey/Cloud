from fastapi import FastAPI
from scan.router import router as scan_router

app = FastAPI(title="Virus Scan Service")
app.include_router(scan_router)

@app.get("/")
def read_root():
    return {"message": "Virus Scan Service is running"}
