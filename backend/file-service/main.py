from fastapi import FastAPI

from upload_file.router import router as upload_router
from delete_file.router import router as delete_file_router
from create_folder.router import router as create_folder_router
from delete_folder.router import router as delete_folder_router
from download_file.router import router as download_file_router
from list_files.router import router as list_files_router
from rename.router import router as rename_file_router
from virus_scan.router import router as virus_scan_router

app = FastAPI(title="File Service")

app.include_router(upload_router)
app.include_router(delete_file_router)
app.include_router(create_folder_router)
app.include_router(delete_folder_router)
app.include_router(download_file_router)
app.include_router(list_files_router)
app.include_router(rename_file_router)
app.include_router(virus_scan_router)

@app.get("/")
def read_root():
    return {"message": "File Service is running"}
