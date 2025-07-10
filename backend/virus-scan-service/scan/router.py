from fastapi import APIRouter, UploadFile, File, HTTPException
from .service import scan_file_with_clamav

router = APIRouter()

@router.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    result = await scan_file_with_clamav(content, file.filename)
    if not result["clean"]:
        return {"clean": False, "detail": result["detail"]}
    return {"clean": True}
